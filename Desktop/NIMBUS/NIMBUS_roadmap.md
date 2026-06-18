# NIMBUS — Build & Learn Roadmap

**Project:** AWS Log Ingestion & IAM Anomaly Detection Framework
**Goal:** Build it from scratch, learning each piece, so you can explain every line in an interview.
**Your setup:** Real AWS (free tier) · New to AWS / Python / ML — so we go in small, working slices.

> Rule of the build: every phase produces something that *runs* and that you *understand* before moving on. You type every line. I explain, structure, and review.

---

## Phase 0 — Safe AWS setup (do this first — it's the only part that can cost money)

- [ ] Create AWS account
- [ ] Enable **MFA on the root user** (phone authenticator app)
- [ ] Set a **billing alarm at $1** (AWS Budgets) so you get emailed before any charge
- [ ] Create a **non-root IAM user** for daily work (never use root day-to-day)
- [ ] Give that user the minimum permissions needed (least privilege — a core security idea)
- [ ] Turn on **CloudTrail** (this is what records the logs we'll analyze)

*What you'll learn:* what IAM, MFA, least privilege, and CloudTrail actually are — by configuring them.

---

## Phase 1 — Stare at one log

- [ ] Do a few actions in the AWS console (log in, create an S3 bucket)
- [ ] Download a single CloudTrail JSON event file
- [ ] Read it together: who did what, when, from which IP, was MFA used

*Goal:* understand one real event. No code yet.

---

## Phase 2 — Parse with Python

- [ ] Write a script that loads the JSON
- [ ] Print a clean table: timestamp · user · action · source IP
- [ ] Handle a folder of multiple log files

*Goal:* Python practice anchored to real data.

---

## Phase 3 — First detection (rules, not ML)

- [ ] Flag: root account used
- [ ] Flag: console login without MFA
- [ ] Flag: access from an unexpected location/IP
- [ ] Flag: IAM policy changes

*Goal:* learn what "anomalous" means before a model decides for you.

---

## Phase 4 — CIS Benchmark mapping

- [ ] Map each rule to a real CIS AWS Benchmark control
- [ ] Output a small report: finding → CIS control → severity

*Goal:* the compliance literacy that makes you sound like an engineer.

---

## Phase 5 — The isolation forest (ML)

- [ ] Collect IAM access events into a feature table
- [ ] Train a scikit-learn isolation forest
- [ ] Review what it flags and *why*
- [ ] Measure precision

*Goal:* ML that isn't magic, because you know the data.

---

## Phase 6 — Polish & tell the story

- [ ] Clean up the pipeline (ingest → detect → report)
- [ ] Write a README
- [ ] Write the résumé bullet from what you *actually* built

---

## Guardrails (read every session)

- Never commit AWS keys to GitHub. Use a `.gitignore` and environment variables.
- Stay in **us-east-1** and free-tier services unless I say otherwise.
- If you ever see an unexpected charge warning — stop and tell me.
- Root account = break-glass only. Daily work = your IAM user.

---

*Progress note: ____ / Phase ___ — (update as you go)*
