# 🔒 Privacy & Compliance Framework (NDPR / NDPA 2023 / GDPR)

> **Scope note:** Nigeria’s data regime evolved from NDPR (2019) to the **Nigeria Data Protection Act (NDPA) 2023**. This framework references **NDPR/NDPA (as applicable)** and **GDPR** for international partners.

## 1. Scope & Data Inventory

ConnectED processes:

- **PII**: Phone numbers.
- **Service Content**: Inbound/outbound SMS text.
- **Delivery Metadata**: Timestamps, message IDs, delivery status.
- **USSD Signals**: Session start/end timestamps, selected menu paths (no device fingerprinting by default).
- **Partner Content**: Uploaded advisories/knowledge packs (non‑PII).

**No children’s data is targeted.** Processing bases include **consent** (USSD registration or documented admin onboarding) and **legitimate interest** (core service operations like delivery receipts and fraud prevention), with an opt‑out at any time.

## 2. Principles

- **Data Minimization** — Collect only what is necessary for service delivery and analytics.
- **Purpose Limitation** — Use data solely for ConnectED services; no unauthorized sharing or secondary use.
- **Integrity & Confidentiality** — Encryption in transit (TLS) and at rest (AES/Fernet); least‑privilege access; key rotation.
- **Accountability** — Logs, audits, DPIA, Records of Processing Activities (ROPA), and breach notification procedures.

## 3. Technical & Organizational Measures

- **Encryption**: Encrypt phone numbers prior to DB write; separate key storage; rotate keys.
- **Pseudonymization**: Hash phone numbers for analytics; avoid raw PII in logs/metrics.
- **Access Control**: Role‑based access (RBAC), short‑lived credentials, just‑in‑time elevation; audit trails for read/export.
- **Secure SDLC**: Secrets in env vars/secret managers; dependency scanning; code review and CI checks.
- **Backups**: Encrypted backups; routine restore tests; backup retention aligned to policy and legal holds.
- **Observability**: Anomaly detection on data export, access spikes, or failed login bursts.

## 4. Consent & Data Subject Rights

- **Opt‑In (Consent Records)**:
  - **USSD** self‑registration: consent auto‑captured with timestamp and session ID.
  - **Manual onboarding** by verified admin: consent recorded via signed form or digital record (date, admin ID, basis).
- **Opt‑Out (as easy as Opt‑In)**:
  - **USSD**: menu option `Opt‑out / Delete my data`.
  - **SMS fallback**: keyword **STOP** (where SMS is used) triggers unsubscribe + deletion workflow.
  - **Admin‑assisted** channel remains available but **cannot be the only route**.
- **Access / Rectification / Erasure / Portability**:

  - **USSD**: `My data` menu offers export/deletion request.
  - **SMS**: keywords `DATA` (export) / `DELETE` (erase).
  - Identity verification performed minimally (reply‑to confirmation and recent session check).

- **Children’s Data**: Not targeted; if discovered, promptly delete and record the incident.

## 5. Processor / Partner Management

- **DPAs** with NGOs/MDAs and telco/hosting providers; define roles (controller/processor) and security duties.
- **Sub‑processors (current examples)**: Microsoft Azure (hosting), Africa’sTalking / Twilio (messaging). Maintain public list with regions and data handling notes; notify on changes.
- **Cross‑Border Transfers**: Use adequacy mechanisms and Standard Contractual Clauses (SCCs) where required; document transfer impact assessments.

## 6. Incident Response

- **Detection**: Alerts for anomalous access/export, privilege escalations, failed login spikes.
- **Response**: Contain, investigate impact, and notify authorities/data subjects within statutory timelines.
- **Postmortem**: Root cause analysis; corrective actions; update playbooks and training.

## 7. Data Retention & Deletion

- **Default Retention**: SMS/USSD content and delivery metadata retained **12 months** (configurable per partner/legal need).
- **Automatic Purge**: Scheduled job (e.g., Celery) deletes data beyond retention; backups roll off per backup policy.
- **Granular Deletion**: Opt‑out or deletion requests remove contact records and linkages; analytics keep only anonymized aggregates.
- **Legal Hold**: Suspension of purge for records under investigation/regulatory request.

## 8. Documentation

- **Public Privacy Policy** aligned with this framework.
- **ROPA** maintained internally.
- **DPIA** for high‑risk domains (e.g., health or finance content) prior to rollout.
- **Consent Ledger**: Immutable log of consent/withdrawal with timestamps and method.

## 9. Compliance Mapping

- **NDPR / NDPA 2023 (Nigeria)**: Lawful basis, consent, data subject rights, security safeguards, cross‑border transfer controls.
- **GDPR (EU)**: Arts. 5–6 (principles/legal bases), 12–23 (rights), 25 (privacy‑by‑design), 30 (ROPA), 32 (security), 33–34 (breach), 44–49 (transfers).
