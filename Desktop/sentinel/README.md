# SENTINEL

Deployable machine-learning security analytics for anomaly detection in historical telemetry.

## Python version

- Recommended local/deployment version: **Python 3.12**
- Docker image is standardized on `python:3.12-slim`.

Current status:
- Phase 1: Streamlit shell, package layout, synthetic demo data.
- Phase 2: CSV ingestion + source-specific mapping (`auth`, `access`) + canonical normalization preview.
- Phase 3: Per-user behavioral features from normalized data (pandas aggregates), with preview and summaries in **Pipeline**.
- Phase 4: IsolationForest on numeric user-feature columns; per-user `anomaly_score`, `is_anomaly`, and short z-score explanations; model kept in memory for the Streamlit session only.
- Phase 5: Deterministic prioritization on scored users—`priority_score` (0–100), `risk_level` (Low / Medium / High / Critical), and `reason_summary`, using ML outputs plus optional feature context (failed logins, off-hours, resource/IP breadth).
- Phase 6: Reporting page with dashboard metrics, risk distribution chart, top-10 highest risk users, and downloadable CSV/TXT triage outputs from `pipeline_risk_df`.
- Phase 7: Stability and deployment readiness (end-to-end pipeline test, session reset utility, Python 3.12 guidance, and docs polish).

## Local setup

1. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run tests (recommended before launching the app):

   ```bash
   python -m pytest tests/ -q
   ```

4. Run the app from the repository root:

   ```bash
   streamlit run app.py
   ```

   The UI loads `src/sentinel` via `sys.path` in `app.py`; you do not need to set `PYTHONPATH` manually.

5. Open **Demo data** in the sidebar, then click **Generate sample** to create synthetic events (optional CSV download).
6. Open **Pipeline** to:
   - upload a CSV
   - select telemetry type (`auth` or `access`)
   - preview source columns and mapping (the app warns early when required columns are missing)
   - run normalization and review canonical output/errors (preview persists for that upload until you change file, type, or clear the uploader)
   - after a successful normalize, click **Build user-level features** for a per-user feature table, numeric summary, and a simple off-hours flag chart
   - then click **Train model and score users** for IsolationForest scores (higher score = more unusual vs other users in the same table), outlier flags, and top-user preview
   - then click **Build prioritized alerts** for rule-based `risk_level` bands and sortable triage reasons (feeds Phase 6 reporting later)
7. Open **Reports** to:
   - review dashboard metrics (Total Users + Critical/High/Medium/Low counts)
   - view a risk-level distribution bar chart and top-10 highest risk users
   - download triage exports (full CSV and plain-text narrative summary)
8. Use **Reset Session** in the sidebar any time you want a clean demo state:
   - clears `demo_*` and `pipeline_*` session keys
   - useful before switching datasets or re-running a walkthrough from scratch

## Run tests

```bash
python -m pytest tests/ -q
```

## Run Streamlit app

```bash
streamlit run app.py
```

## Docker (Python 3.12)

```bash
docker build -t sentinel:local .
docker run --rm -p 8501:8501 sentinel:local
```

Then open http://localhost:8501.

## Deployment guidance

- Primary demo target: **Streamlit Community Cloud**
  - Set app file to `app.py`
  - Use dependencies from `requirements.txt`
  - Use Python **3.12** in app settings when available
- Secondary target: Docker host (Render/Cloud Run style) using the provided `Dockerfile`.

Test focus:
- `tests/test_normalize.py` — Phase 2 mapping and validation (required columns, timestamps, empty uploads, invalid mappings).
- `tests/test_features.py` — Phase 3 user features (happy path, empty frame, missing columns, all-null `user_id`, access-only users, business vs off-hours).
- `tests/test_scoring.py` — Phase 4 scoring (valid data, empty table, missing `user_id`, no feature columns, single-user neutral path, NaN imputation, two-user train).
- `tests/test_risk.py` — Phase 5 prioritization (empty scored frame, missing columns, stable sort, escalation vs quiet baseline, features optional).
- `tests/test_reports.py` — Phase 6 exports (`build_csv_bytes`, `build_text_summary`, and summary content checks).
- `tests/test_pipeline_e2e.py` — Phase 7 lightweight end-to-end flow from synthetic generation through report export.

## Project docs

- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — product scope and architecture
- [BUILD_PLAN.md](BUILD_PLAN.md) — phased delivery
- [SESSION_UPDATES.md](SESSION_UPDATES.md) — session memory

## Disclaimer

Synthetic demo data is **fictional**. Do not treat generated rows as evidence of real security incidents.
