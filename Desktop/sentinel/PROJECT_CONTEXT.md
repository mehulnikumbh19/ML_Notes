# SENTINEL Project Context

## 1. Project identity
- Project name: SENTINEL
- Category: Machine Learning + Security
- Product type: Deployable security analytics application
- Primary goal: Detect abnormal behavior in historical security telemetry and prioritize likely security incidents for analysts.

## 2. Problem statement
Traditional static rules miss subtle attacker behavior such as low-and-slow abuse, unusual access timing, privilege misuse, approval mismatches, and compromised-account behavior. SENTINEL improves detection by learning normal behavior from telemetry and scoring anomalies.

## 3. MVP definition
SENTINEL v1 must do all of the following:
1. Ingest telemetry files from CSV uploads.
2. Normalize different telemetry types into one canonical schema.
3. Engineer security-relevant features.
4. Train an unsupervised anomaly model.
5. Score new or uploaded data.
6. Prioritize anomalies into analyst-friendly risk levels.
7. Show results in a browser dashboard.
8. Export a triage report.
9. Be deployable publicly.

## 4. Non-goals for v1
Do not build these in v1 unless explicitly requested later:
- Real-time streaming ingestion
- Production SSO
- SIEM integrations
- EDR integrations
- Distributed model training
- Multi-tenant RBAC
- Deep learning pipelines
- Live alerting to email/Slack
- Enterprise-scale data engineering

## 5. Target users
- SOC analyst
- Security engineer
- Hiring manager / interviewer viewing a portfolio project

## 6. Recommended implementation approach
Build the first complete version as a **single Python application with Streamlit UI and modular backend code**.
Reason:
- Lowest implementation complexity
- Fastest path to a hosted demo
- Best fit for a beginner using coding agents
- Easy to deploy on Streamlit Community Cloud first
- Still Docker-friendly for Render or Cloud Run later

## 7. Recommended tech stack
- Language: Python
- UI: Streamlit
- Data processing: pandas, numpy
- ML: scikit-learn (IsolationForest as baseline)
- Validation / config: pydantic
- Charts: plotly
- Storage for local MVP: SQLite
- Testing: pytest
- Packaging / deploy: requirements.txt + Dockerfile

## 8. Core product capabilities
### 8.1 Data ingestion
Support these telemetry categories for CSV upload:
- Authentication / login logs
- Access logs
- Control-execution / approval logs
- Endpoint or network event logs

### 8.2 Canonical schema
Every normalized record should map into a common structure where possible:
- event_id
- event_type
- timestamp
- user_id
- username
- role
- source_ip
- device_id
- hostname
- geo_country
- action
- resource
- resource_sensitivity
- approval_required
- approval_present
- success
- failure_reason
- bytes_in
- bytes_out
- endpoint_process
- network_destination
- raw_source

### 8.3 Feature engineering targets
Engineer features such as:
- login_count_1h
- failed_auth_burst_15m
- off_hours_access_flag
- new_ip_for_user_flag
- new_device_for_user_flag
- role_deviation_flag
- privileged_action_flag
- approval_mismatch_flag
- unusual_resource_access_flag
- endpoint_process_rarity
- bytes_out_zscore
- auth_failure_ratio
- daily_event_volume_delta

### 8.4 Modeling approach
Initial model:
- Train IsolationForest on engineered features.
- Standardize numeric features when appropriate.
- Keep model explainability simple and practical.
- Add rule-based enrichments alongside ML score.

### 8.5 Risk prioritization
Create a final risk score that combines:
- anomaly score
- privilege sensitivity
- approval mismatch
- off-hours behavior
- failed-auth bursts
- sensitive resource access
- new IP / new device indicators

Map final score into:
- Low
- Medium
- High
- Critical

### 8.6 Analyst outputs
The product must show:
- Overview metrics
- Alert table
- Drill-down detail view
- Feature evidence behind each anomaly
- Exportable triage report

## 9. Default repository structure
```text
sentinel/
  app.py
  requirements.txt
  Dockerfile
  README.md
  PROJECT_CONTEXT.md
  SESSION_UPDATES.md
  data/
    sample_auth_logs.csv
    sample_access_logs.csv
    sample_control_logs.csv
    sample_endpoint_events.csv
  src/sentinel/
    config.py
    schemas.py
    ingest/
      loaders.py
      normalize.py
      synthetic.py
    features/
      pipeline.py
      auth_features.py
      behavior_features.py
      risk_features.py
    models/
      train.py
      score.py
      explain.py
    risk/
      prioritization.py
      rules.py
    reports/
      triage.py
      export.py
    storage/
      sqlite_store.py
    ui/
      views.py
  tests/
    test_normalize.py
    test_features.py
    test_scoring.py
    test_risk.py
```

## 10. Product quality bar
Before any phase is considered complete:
- The app must run locally.
- The relevant feature must work through the UI.
- At least one meaningful test must exist for the new behavior.
- The README must stay accurate.
- No fake claims about accuracy are allowed.
- Demo data must be available so the app can be shown without external sources.

## 11. Delivery strategy
### Phase 1
Repository setup, project memory files, basic app shell, sample synthetic data.

### Phase 2
Normalization pipeline and canonical schema.

### Phase 3
Feature engineering pipeline.

### Phase 4
Baseline anomaly model and scoring.

### Phase 5
Risk prioritization and analyst explanations.

### Phase 6
Dashboard and report export.

### Phase 7
Testing, cleanup, Dockerization, deployment.

## 12. Tool usage policy
### Use Cursor for
- fast code generation
- routine refactors
- tests
- file-by-file implementation
- small bug fixes
- local iteration

### Use Antigravity for
- architecture planning
- reviewing larger implementation plans
- browser-based app testing
- deployment help
- documentation lookup
- tough debugging after repeated failures

## 13. Cost-control policy
Default to cheaper / faster models first.
Only escalate to stronger thinking models when:
- the same bug survives two focused attempts
- architecture tradeoffs are unclear
- deployment keeps failing for unclear reasons
- the agent cannot produce a coherent plan

## 14. Current status
- Project stage: COMPLETE / DEPLOYMENT READY
- Phase 3: Completed and approved by user (2026-03-23); feature engineering pipeline is in the app with tests per approved session 2026-03-23-05.
- Phase 4: Completed and approved by user (2026-03-23); IsolationForest scoring on the per-user feature table, Pipeline UI, and tests per approved session 2026-03-23-06.
- Phase 5: Completed and approved by user (2026-03-23); deterministic prioritization (`priority_score`, `risk_level`, `reason_summary`) in `src/sentinel/risk/prioritization.py`, Pipeline alerts UI, and tests per approved session 2026-03-23-07.
- Phase 6: Completed and approved by user (2026-03-23); Reports page in `app.py` consumes `st.session_state["pipeline_risk_df"]` for dashboard metrics, risk distribution chart, top-10 users, and CSV/TXT triage exports via `src/sentinel/reports/export.py`, with tests in `tests/test_reports.py` per approved session 2026-03-23-08.
- Phase 7: Completed and approved by user (2026-03-23); added lightweight end-to-end pipeline coverage in `tests/test_pipeline_e2e.py`, reusable demo/session reset utility in `src/sentinel/utils/state.py` wired in `app.py`, Python 3.12/deployment README polish, and minimal safer CSV upload messaging per approved session 2026-03-23-09.
- Active phase: None (all planned MVP phases complete)
- Current milestone: Deployment/demo handoff and optional hosting setup verification.
- Deployment target for first public demo: Streamlit Community Cloud
- Secondary deployment target: Render or Google Cloud Run via Docker
- Final project status note: End-to-end pipeline is complete, reporting and exports are complete, E2E test coverage is added, and the MVP is ready for deployment/demo use.

## 15. Last confirmed session snapshot
- Date: 2026-03-23
- Summary: Phase 7 completed and approved by user — hardening and deployment-readiness updates include a lightweight end-to-end regression test from synthetic generation through report exports (`tests/test_pipeline_e2e.py`), reusable session reset helper (`src/sentinel/utils/state.py`) integrated into sidebar reset behavior in `app.py`, and documentation polish for Python 3.12 setup/deployment guidance; verification at approval: 41 tests passing.
- Next recommended action: Deploy to Streamlit Community Cloud for final demo handoff; optionally validate Docker deployment on Render/Cloud Run.

## 16. Rules for agents reading this file
1. Read this file at the start of every substantial task.
2. Read SESSION_UPDATES.md immediately after this file.
3. Treat the latest APPROVED session entry as the most recent source of truth.
4. Do not change stack or scope without documenting why.
5. Keep implementation simple, modular, and resume-friendly.
6. At session close, draft a new pending update and ask for approval.
