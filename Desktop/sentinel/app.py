"""SENTINEL Streamlit entrypoint."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import streamlit as st
import pandas as pd
import plotly.express as px

from sentinel.ingest.synthetic import demo_columns, generate_demo_events
from sentinel.ingest.normalize import (
    SOURCE_MAPPINGS,
    normalize_uploaded_csv,
    required_source_columns,
)
from sentinel.features import (
    build_user_features,
    feature_distribution_counts,
    feature_numeric_summary,
)
from sentinel.models import score_user_feature_table
from sentinel.risk import prioritize_alerts
from sentinel.reports import build_csv_bytes, build_text_summary
from sentinel.utils import clear_demo_session_state

st.set_page_config(page_title="SENTINEL", page_icon="🛡️", layout="wide")

st.sidebar.title("SENTINEL")
if st.sidebar.button("Reset Session", help="Clear demo and pipeline state for a fresh run."):
    cleared_count = clear_demo_session_state(st.session_state)
    st.sidebar.success(f"Session reset complete ({cleared_count} keys cleared).")

page = st.sidebar.radio(
    "Navigate",
    ("Home", "Demo data", "Pipeline", "Reports"),
    index=0,
)

if page == "Home":
    st.title("SENTINEL")
    st.write(
        "Machine-learning security analytics for historical telemetry. "
        "The app includes Phase 1 demo data, Phase 2 CSV normalization, Phase 3 user-level features, "
        "Phase 4 IsolationForest scoring, and Phase 5 deterministic risk bands on the **Pipeline** page. "
        "Phase 6 adds analyst-friendly reporting on the **Reports** page."
    )
    st.info(
        "Use the sidebar for **Demo data** (synthetic sample), **Pipeline** (CSV upload and normalization), "
        "or **Reports** (Phase 6 analyst output)."
    )

elif page == "Demo data":
    st.header("Synthetic demo telemetry")
    st.caption("Generated data is fictional and for UI demos only—not real security events.")

    n = st.slider("Number of events", min_value=10, max_value=500, value=50, step=10)
    seed = st.number_input("Random seed (optional)", value=42, min_value=0, step=1)
    use_seed = st.checkbox("Fix seed for reproducible sample", value=True)

    if st.button("Generate sample", type="primary"):
        df = generate_demo_events(n=n, seed=int(seed) if use_seed else None)
        st.session_state["demo_df"] = df

    if "demo_df" in st.session_state:
        df = st.session_state["demo_df"]
        st.metric("Rows", len(df))
        st.dataframe(df.head(20), use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="sentinel_demo_events.csv",
            mime="text/csv",
        )
    with st.expander("Column reference (Phase 2 schema)"):
        st.write(demo_columns())

elif page == "Pipeline":
    st.header("Pipeline")
    st.subheader("Phase 2–5: Normalize, features, anomaly scores, risk prioritization")
    st.write(
        "Upload CSV telemetry, map to the canonical schema, build per-user behavioral features, "
        "train an IsolationForest for this session, then apply simple rule-based priority bands for triage."
    )

    telemetry_type = st.selectbox(
        "Telemetry type",
        options=("auth", "access"),
        help="Select the source profile used for column mapping.",
    )
    st.caption(f"Expected source columns for `{telemetry_type}`: {', '.join(required_source_columns(telemetry_type))}")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is None:
        st.info("Upload a CSV file to begin.")
        clear_demo_session_state(st.session_state, exact_keys=(), prefixes=("pipeline_",))
    else:
        should_attempt_read = True
        if getattr(uploaded_file, "size", 0) == 0:
            st.error("Uploaded file is empty. Please choose a non-empty CSV.")
            clear_demo_session_state(st.session_state, exact_keys=(), prefixes=("pipeline_",))
            should_attempt_read = False
        source_df = None
        try:
            if should_attempt_read:
                source_df = pd.read_csv(uploaded_file)
        except pd.errors.EmptyDataError:  # pragma: no cover - UI-only branch
            st.error("The uploaded CSV has no rows to parse. Please upload a valid CSV with data.")
            source_df = None
        except pd.errors.ParserError as exc:  # pragma: no cover - UI-only branch
            st.error(f"CSV parsing failed. Please check delimiter/quoting and retry. Details: {exc}")
            source_df = None
        except Exception as exc:  # pragma: no cover - UI-only branch
            st.error(f"Could not read CSV. Please confirm it is a valid CSV file. Details: {exc}")
            source_df = None

        if source_df is not None:
            missing_required = [c for c in required_source_columns(telemetry_type) if c not in source_df.columns]
            if missing_required:
                st.warning(
                    "The uploaded file is missing required columns for "
                    f"`{telemetry_type}`: {', '.join(missing_required)}. "
                    "Normalization will fail until these columns are present."
                )

            upload_sig = (
                telemetry_type,
                uploaded_file.name,
                len(source_df),
                tuple(source_df.columns),
            )

            prev_feat_sig = st.session_state.get("pipeline_feat_sig")
            if prev_feat_sig is not None and prev_feat_sig != upload_sig:
                st.session_state.pop("pipeline_feat_df", None)
                st.session_state.pop("pipeline_feat_errs", None)
                st.session_state.pop("pipeline_feat_sig", None)
                st.session_state.pop("pipeline_score_df", None)
                st.session_state.pop("pipeline_score_errs", None)
                st.session_state.pop("pipeline_score_sig", None)
                st.session_state.pop("pipeline_risk_df", None)
                st.session_state.pop("pipeline_risk_errs", None)
                st.session_state.pop("pipeline_risk_sig", None)

            st.write("Source column mapping preview")
            mapping_df = pd.DataFrame(
                {
                    "canonical_field": list(SOURCE_MAPPINGS[telemetry_type].keys()),
                    "source_column": list(SOURCE_MAPPINGS[telemetry_type].values()),
                }
            )
            st.dataframe(mapping_df, use_container_width=True)

            st.write("Uploaded source preview")
            st.caption(f"Rows: {len(source_df)} | Columns: {len(source_df.columns)}")
            st.dataframe(source_df.head(20), use_container_width=True)
            st.code(", ".join(source_df.columns), language="text")

            if st.button("Run normalization", type="primary"):
                result = normalize_uploaded_csv(source_df, telemetry_type)
                st.session_state["pipeline_norm_result"] = result
                st.session_state["pipeline_norm_sig"] = upload_sig

            saved_sig = st.session_state.get("pipeline_norm_sig")
            saved_result = st.session_state.get("pipeline_norm_result")
            if saved_sig == upload_sig and saved_result is not None:
                result = saved_result
                if result.errors:
                    st.session_state.pop("pipeline_feat_df", None)
                    st.session_state.pop("pipeline_feat_errs", None)
                    st.session_state.pop("pipeline_feat_sig", None)
                    st.session_state.pop("pipeline_score_df", None)
                    st.session_state.pop("pipeline_score_errs", None)
                    st.session_state.pop("pipeline_score_sig", None)
                    st.session_state.pop("pipeline_risk_df", None)
                    st.session_state.pop("pipeline_risk_errs", None)
                    st.session_state.pop("pipeline_risk_sig", None)
                    st.error("Normalization failed with validation errors:")
                    for err in result.errors:
                        st.write(f"- {err}")
                else:
                    st.success("Normalization completed successfully.")
                st.write("Normalized dataset preview (saved for this upload and telemetry type)")
                st.dataframe(result.normalized_df.head(20), use_container_width=True)

                if not result.errors:
                    st.divider()
                    st.markdown("### Phase 3: User-level features")
                    st.caption(
                        "Aggregates normalized rows per `user_id`: login volume, failure ratio, "
                        "off-hours activity, resource and IP diversity, and mean events per active day."
                    )
                    if st.button("Build user-level features", key="build_features"):
                        st.session_state.pop("pipeline_score_df", None)
                        st.session_state.pop("pipeline_score_errs", None)
                        st.session_state.pop("pipeline_score_sig", None)
                        st.session_state.pop("pipeline_risk_df", None)
                        st.session_state.pop("pipeline_risk_errs", None)
                        st.session_state.pop("pipeline_risk_sig", None)
                        feats, ferrs = build_user_features(result.normalized_df)
                        st.session_state["pipeline_feat_df"] = feats
                        st.session_state["pipeline_feat_errs"] = ferrs
                        st.session_state["pipeline_feat_sig"] = upload_sig

                    if st.session_state.get("pipeline_feat_sig") == upload_sig:
                        ferrs = st.session_state.get("pipeline_feat_errs") or []
                        feats = st.session_state.get("pipeline_feat_df")
                        if ferrs:
                            st.error("Feature build failed:")
                            for err in ferrs:
                                st.write(f"- {err}")
                        elif feats is not None:
                            if feats.empty:
                                st.warning("No feature rows produced (normalized data was empty).")
                            else:
                                st.metric("Users in feature table", len(feats))
                                st.write("Feature preview")
                                st.dataframe(feats.head(25), use_container_width=True)
                                st.write("Numeric summary (count / mean / std / min / max)")
                                summary = feature_numeric_summary(feats)
                                if summary.empty:
                                    st.caption("No numeric summary available.")
                                else:
                                    st.dataframe(summary, use_container_width=True)
                                dist = feature_distribution_counts(feats)
                                oh = dist.get("off_hours_access_flag")
                                if oh is not None and not oh.empty:
                                    st.write("Off-hours flag distribution (`1` = any off-hours event)")
                                    st.bar_chart(oh.to_frame(name="users"))

                                st.divider()
                                st.markdown("### Phase 4: Anomaly scores (IsolationForest)")
                                st.caption(
                                    "Trains on the numeric Phase 3 columns only (one row per user). "
                                    "**anomaly_score**: higher means the forest considers the user more unusual vs peers "
                                    "(not a calibrated probability). **is_anomaly**: forest outlier flag for this run. "
                                    "**anomaly_explanation**: simple z-score hints vs all users in this table."
                                )
                                if st.button("Train model and score users", key="score_anomalies"):
                                    st.session_state.pop("pipeline_risk_df", None)
                                    st.session_state.pop("pipeline_risk_errs", None)
                                    st.session_state.pop("pipeline_risk_sig", None)
                                    scored, serrs, _sinfo = score_user_feature_table(feats)
                                    st.session_state["pipeline_score_df"] = scored
                                    st.session_state["pipeline_score_errs"] = serrs
                                    st.session_state["pipeline_score_sig"] = upload_sig

                                if st.session_state.get("pipeline_score_sig") == upload_sig:
                                    serrs = st.session_state.get("pipeline_score_errs") or []
                                    scored = st.session_state.get("pipeline_score_df")
                                    if serrs:
                                        st.error("Scoring failed:")
                                        for err in serrs:
                                            st.write(f"- {err}")
                                    elif scored is not None:
                                        if scored.empty:
                                            st.warning("No scored rows (feature table was empty).")
                                        else:
                                            n_flag = int(scored["is_anomaly"].sum())
                                            st.metric("Users flagged as anomalies (this run)", n_flag)
                                            top = scored.sort_values(
                                                "anomaly_score", ascending=False
                                            ).head(25)
                                            st.write("Top 25 users by anomaly score")
                                            st.dataframe(top, use_container_width=True)
                                            st.write("Full scored table (sortable in the grid)")
                                            st.dataframe(scored, use_container_width=True)

                                            st.divider()
                                            st.markdown("### Phase 5: Prioritized alerts")
                                            st.caption(
                                                "Deterministic blend of **anomaly_score**, **is_anomaly**, and—when available—"
                                                "**failed_login_ratio**, **off_hours_access_flag**, **unique_resource_count**, "
                                                "and **ip_diversity** from the feature table. Produces **priority_score** (0–100), "
                                                "**risk_level** (Low / Medium / High / Critical), and **reason_summary**."
                                            )
                                            if st.button("Build prioritized alerts", key="prioritize_risk"):
                                                alerts, rerrs = prioritize_alerts(scored, feats)
                                                st.session_state["pipeline_risk_df"] = alerts
                                                st.session_state["pipeline_risk_errs"] = rerrs
                                                st.session_state["pipeline_risk_sig"] = upload_sig

                                            if st.session_state.get("pipeline_risk_sig") == upload_sig:
                                                rerrs = st.session_state.get("pipeline_risk_errs") or []
                                                alerts = st.session_state.get("pipeline_risk_df")
                                                if rerrs:
                                                    st.error("Prioritization failed:")
                                                    for err in rerrs:
                                                        st.write(f"- {err}")
                                                elif alerts is not None:
                                                    if alerts.empty:
                                                        st.warning("No alert rows (scored table was empty).")
                                                    else:
                                                        crit = int((alerts["risk_level"] == "Critical").sum())
                                                        high = int((alerts["risk_level"] == "High").sum())
                                                        st.metric("Critical-band users", crit)
                                                        st.metric("High-band users", high)
                                                        top_alert = alerts.head(25)
                                                        st.write("Top 25 prioritized users")
                                                        st.dataframe(top_alert, use_container_width=True)
                                                        st.write("Full prioritized alert table")
                                                        st.dataframe(alerts, use_container_width=True)
else:
    st.header("Reports")
    st.subheader("Phase 6: Reporting and analyst output")
    st.write(
        "Review prioritized alerts from the Pipeline run, then export triage outputs "
        "for demo-ready analyst handoff."
    )

    alerts_df = st.session_state.get("pipeline_risk_df")
    if alerts_df is None:
        st.info(
            "No prioritized alerts found in this session yet. "
            "Run the Pipeline page through **Build prioritized alerts** first."
        )
    elif isinstance(alerts_df, pd.DataFrame) and alerts_df.empty:
        st.info("Prioritized alerts are empty for this run. Try a different dataset in Pipeline.")
    else:
        assert isinstance(alerts_df, pd.DataFrame)
        run_date = date.today().strftime("%Y%m%d")

        st.markdown("### Dashboard overview")
        total_users = int(alerts_df["user_id"].nunique()) if "user_id" in alerts_df.columns else len(alerts_df)
        risk_counts = (
            alerts_df["risk_level"].value_counts().reindex(["Critical", "High", "Medium", "Low"], fill_value=0)
            if "risk_level" in alerts_df.columns
            else pd.Series([0, 0, 0, 0], index=["Critical", "High", "Medium", "Low"])
        )

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Users Analyzed", total_users)
        c2.metric("Critical Alerts", int(risk_counts["Critical"]))
        c3.metric("High Alerts", int(risk_counts["High"]))
        c4.metric("Medium Alerts", int(risk_counts["Medium"]))
        c5.metric("Low Alerts", int(risk_counts["Low"]))

        st.markdown("### Risk distribution")
        chart_df = risk_counts.rename_axis("risk_level").reset_index(name="count")
        fig = px.bar(
            chart_df,
            x="risk_level",
            y="count",
            category_orders={"risk_level": ["Critical", "High", "Medium", "Low"]},
            title="Users by risk level",
        )
        fig.update_layout(xaxis_title="Risk level", yaxis_title="User count")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Top-10 highest risk users")
        top_cols = ["user_id", "risk_level", "priority_score", "reason_summary"]
        existing_cols = [c for c in top_cols if c in alerts_df.columns]
        top10 = alerts_df.head(10)
        if existing_cols:
            st.dataframe(top10[existing_cols], use_container_width=True)
        else:
            st.dataframe(top10, use_container_width=True)

        st.markdown("### Export triage outputs")
        csv_bytes = build_csv_bytes(alerts_df)
        txt_summary = build_text_summary(alerts_df, run_date=run_date)
        st.download_button(
            "Download triage CSV",
            data=csv_bytes,
            file_name=f"sentinel_triage_report_{run_date}.csv",
            mime="text/csv",
        )
        st.download_button(
            "Download narrative summary (TXT)",
            data=txt_summary.encode("utf-8"),
            file_name=f"sentinel_triage_summary_{run_date}.txt",
            mime="text/plain",
        )
