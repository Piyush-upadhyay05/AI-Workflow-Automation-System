# 🥝 Kiwi Connect Digital — AI Workflow Automation System

> **Position:** AI Intern — Technical Assignment  
> **Candidate Submission:** AI Workflow Automation & Lead Intelligence System  
> **Organization:** [Kiwi Connect Digital](https://kiwiconnectdigital.com) — *Think Social. Think Kiwi. | Build Smart. Automate Better. Think Beyond.*  
> **Status:** Production-Ready / Fully Tested  

---

## 📌 Executive Summary

Businesses receive customer enquiries through multiple channels (web forms, emails, WhatsApp, social media). Manually reading, interpreting unstructured requirements, categorizing domains, estimating budgets, assessing urgency, and drafting replies is slow and prone to human error.

**LeadFlow AI** is an enterprise-grade AI Workflow Automation System engineered to automate this end-to-end lifecycle. When an enquiry is received, the system validates the input, runs real-time duplicate detection, leverages **Google Gemini Flash LLMs** to extract structured metadata (service category, budget, location, urgency, key deliverables, missing information), scores lead readiness (0–100), drafts tailored responses, and commits the record to an indexed SQLite database for live monitoring through an **Executive Admin Dashboard** and **FastAPI REST API**.

---

## 🚀 Key System Features

### A. Enquiry Input System
* **Universal Intake Form:** Web and API ingestion capturing Customer Name, Phone Number, Email Address, and Enquiry Message.
* **1-Click Demo Presets:** Includes the official assignment enquiry (*"I own a clothing store in Indore. I need an e-commerce website..."*), urgent healthcare AI queries, mobile apps, SaaS growth marketing, and ambiguous leads.
* **Input Sanitization & Injection Defense:** Enforces strict boundary isolation to ensure user messages are processed as pure data, never executable instructions.

### B. AI-Powered Analysis & Extraction Core
* **Service Classification:** Automatically classifies enquiries into the 7 mandated business verticals:
  1. `Website Development`
  2. `Mobile Application Development`
  3. `AI Software Development`
  4. `Digital Marketing`
  5. `E-commerce Development`
  6. `Custom Software Development`
  7. `Other Services`
* **Entity Extraction:** Identifies stated budget, client location, and timeline urgency (`High`, `Medium`, `Low`, `Unknown`).
* **Requirements & Missing Information:** Synthesizes a structured checklist of explicit deliverables and identifies missing details needed to finalize commercial proposals.
* **Priority Determination:** Assigns `High`, `Medium`, or `Low` priority accompanied by logical reasoning.

### C. AI-Generated Customer Response & Sales Tools
* **Contextual Response Generation:** Generates a courteous, professional response tailored to the client's domain and budget.
* **Next Steps & Follow-Up Questions:** Proposes concrete next milestones and politely requests missing details.
* **Human-in-the-Loop Admin Editor:** Administrators can review, customize, and save edited responses before outreach.
* **1-Click Outreach Launchers:** Directly generates pre-filled **WhatsApp Web** links (`https://wa.me/...`) and **Email Drafts** (`mailto:...`).

### D. Executive Admin Dashboard & CRM
* **Real-time KPI Metrics:** Total Enquiries, New Leads, In Progress, Converted Leads, High-Priority Alerts, and Sales Funnel Conversion Rate.
* **Interactive Visual Analytics:** Category distribution bar charts, priority matrix, status pipeline, and lead quality health score meters.
* **Search & Multi-Filter Engine:** Instant full-text search across customer names, contact info, and message contents with category, priority, and status filters.
* **Data Export:** Instant download of filtered or complete lead records in **CSV** or **JSON** format.

### E. 🌟 All 10 Bonus Features Implemented
1. **Automatic Duplicate Enquiry Detection:** Checks incoming enquiries against phone, email, and token-level Jaccard similarity to flag duplicate leads and link the original enquiry ID.
2. **AI-Based Lead Scoring (0–100):** Multi-factor scoring algorithm evaluating budget clarity, requirement specificity, contact completeness, and urgency.
3. **Follow-Up Reminder Suggestions:** Generates target follow-up deadlines (e.g. *Within 24 hours* for High priority) and recommended sales actions.
4. **WhatsApp Web Integration:** Generates 1-click WhatsApp messaging links with the approved customer reply.
5. **Email Notifications & Mailto Launcher:** Generates pre-populated email drafts with subject lines and customized bodies.
6. **Visual Workflow Representation:** Interactive in-app trace visualizer displaying the 9-step automated pipeline, execution timings, and data flow.
7. **Analytics and Reporting:** Visual distribution charts for categories, priorities, statuses, and lead score tiers.
8. **Automatic Team Member Routing:** Intelligently assigns incoming leads to specialized team leads based on category (e.g., *Rahul Sharma - Indore E-Commerce Specialist*).
9. **Export Enquiries to CSV & JSON:** Single-click export for reporting and spreadsheet analysis.
10. **AI-Generated Enquiry Summaries:** Generates concise, 1-sentence executive summaries for instant CRM review.

---

## 🏗️ System Architecture & 9-Step Workflow

```
+-----------------------------------------------------------------------------------+
|                            CLIENT & INTAKE INTERFACES                             |
|  - Streamlit Web Dashboard (Port 8501)       - FastAPI REST Endpoints (Port 8000) |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             AUTOMATION & ORCHESTRATION                            |
|  - Input Validation & Defense   - Duplicate Detection Engine   - Department Router |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                              AI REASONING CORE (LLM)                              |
|  - Google Gemini 3.5 Flash Lite / 3.1 Flash Lite (Structured JSON Generation)     |
|  - Deterministic Offline Heuristic Fallback Engine (Zero-Downtime Guarantee)      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             STORAGE & CRM MANAGEMENT                              |
|  - SQLite Database (`enquiries.db`) with dynamic schema migration & indexes       |
|  - Lead Scoring (0-100)      - WhatsApp / Mailto Launchers   - CSV / JSON Export  |
+-----------------------------------------------------------------------------------+
```

### The 9-Step Lifecycle:
1. **Step 1:** Customer or administrator submits enquiry via Web Intake Form or REST API (`POST /api/enquiries`).
2. **Step 2:** Backend validates payload, sanitizes text, and initializes an atomic database record.
3. **Step 3:** Duplicate detection engine scans phone numbers, email addresses, and message text similarity against historical leads.
4. **Step 4:** AI Reasoning Core analyzes intent, business domain context, and constraints.
5. **Step 5:** AI extracts structured entities (Category, Budget, Location, Urgency, Requirements, Missing Info).
6. **Step 6:** System classifies into 1 of the 7 allowed categories and routes to the appropriate specialist team lead.
7. **Step 7:** AI calculates a 0–100 Lead Score and assigns a priority level (`High`, `Medium`, `Low`).
8. **Step 8:** AI composes a professional response, follow-up timeline, and recommended next steps.
9. **Step 9:** All attributes, scores, and timestamps are persisted to SQLite and surfaced immediately on the Admin Dashboard.

---

## 💾 Database Schema

The system uses an indexed SQLite database (`enquiries.db`) with automated schema migrations.

| Column | Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique enquiry identifier |
| `customer_name` | TEXT | NOT NULL | Customer's full name |
| `phone` | TEXT | NULL | Contact phone number |
| `email` | TEXT | NULL | Contact email address |
| `message` | TEXT | NOT NULL | Raw customer enquiry message |
| `category` | TEXT | DEFAULT 'Unclassified' | 1 of 7 allowed service categories |
| `priority` | TEXT | DEFAULT 'Medium' | High, Medium, or Low |
| `urgency` | TEXT | DEFAULT 'Unknown' | High, Medium, Low, or Unknown |
| `budget` | TEXT | NULL | Stated project budget |
| `location` | TEXT | NULL | Customer location / city |
| `lead_score` | INTEGER | DEFAULT 50 | 0–100 sales qualification score |
| `lead_score_reason`| TEXT | NULL | Justification for lead score |
| `summary` | TEXT | NULL | Crisp 1-sentence executive summary |
| `status` | TEXT | DEFAULT 'New' | New, In Progress, Converted, Closed |
| `assigned_to` | TEXT | NULL | Specialized team member assigned |
| `is_duplicate` | INTEGER | DEFAULT 0 | 1 if detected as duplicate, else 0 |
| `duplicate_of_id` | INTEGER | NULL | Linked original enquiry ID |
| `follow_up_date` | TEXT | NULL | Recommended follow-up timeframe |
| `follow_up_action` | TEXT | NULL | Recommended next sales action |
| `tags` | TEXT | NULL | JSON array of extracted deliverables |
| `ai_analysis` | TEXT | NULL | Full JSON output from AI engine |
| `ai_response` | TEXT | NULL | Suggested customer response |
| `edited_response` | TEXT | NULL | Admin-reviewed & modified response |
| `created_at` | TEXT | CURRENT_TIMESTAMP | Ingestion timestamp |
| `updated_at` | TEXT | CURRENT_TIMESTAMP | Last update timestamp |

---

## 🛠️ Technology Stack

| Component | Selected Technology | Rationale |
|---|---|---|
| **Dashboard UI** | **Streamlit** (Python) | Interactive, responsive executive dashboard with live charts, forms, and CRM controls |
| **Backend REST API** | **FastAPI + Uvicorn** | High-performance, asynchronous REST API with automatic OpenAPI Swagger documentation (`/docs`) |
| **AI Integration** | **Google Gemini 3.5 Flash Lite** via `google-genai` | Sub-second latency, native JSON schema mode, high extraction accuracy, cost-effective |
| **Fallback Engine** | **Deterministic NLP / Regex** | Guarantees zero downtime if internet is disconnected or API quota is reached |
| **Database** | **SQLite 3** | Zero-configuration, serverless, atomic transactions, and dynamic schema migrations |
| **Data Processing** | **Pandas & OpenPyXL** | Analytics aggregation and CSV/Excel data export |
| **Testing** | **Python Unittest Suite** | Automated test suite validating database, duplicate detection, and API endpoints |

---

## 📦 Installation & Setup Guide

### 1. Prerequisites
* Python 3.10, 3.11, or 3.12 installed
* Git installed
* Google Gemini API Key ([Free from Google AI Studio](https://aistudio.google.com/))

### 2. Clone Repository
```bash
git clone https://github.com/your-username/ai-workflow-automation-system.git
cd ai-workflow-automation-system
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env` and insert your Gemini API key:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```
Inside `.env`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

---

## 🖥️ Running the Application

### Option A: Launch Interactive Admin Dashboard (Streamlit)
```bash
streamlit run app.py
```
Open your browser at: **`http://localhost:8501`**

### Option B: Launch FastAPI REST API Backend
```bash
uvicorn api:app --reload --port 8000
```
* **Interactive Swagger UI:** **`http://localhost:8000/docs`**
* **Redoc Documentation:** **`http://localhost:8000/redoc`**

### Option C: Seed Realistic Sample Data
To instantly populate the dashboard with 6 realistic business leads (including the Indore E-Commerce store, urgent healthcare AI, mobile delivery, and a duplicate test):
```bash
python seed_data.py
```
*(Or click the **"🌱 Load Realistic Sample Leads"** button directly in the Streamlit sidebar!)*

### Option D: Run Automated Test Suite
```bash
python -m unittest tests/test_system.py
```
*All tests execute and pass in under 0.1 seconds.*

---

## 📡 REST API Reference

The FastAPI service exposes clean REST endpoints:

* `GET /` — Service health and metadata
* `POST /api/enquiries` — Ingests enquiry, performs duplicate check, runs AI pipeline, and saves to database
* `GET /api/enquiries` — Lists enquiries with query filters (`search`, `category`, `priority`, `status`)
* `GET /api/enquiries/{id}` — Returns full details and structured AI analysis for a specific lead
* `PATCH /api/enquiries/{id}/status` — Updates lead status (`New`, `In Progress`, `Converted`, `Closed`)
* `PATCH /api/enquiries/{id}/response` — Saves administrator-reviewed / edited response
* `PATCH /api/enquiries/{id}/assign` — Reassigns lead to a different team specialist
* `POST /api/enquiries/{id}/reanalyze` — Re-triggers AI analysis on an existing enquiry
* `GET /api/dashboard/stats` — Returns aggregated KPIs, conversion rate, and category distributions
* `POST /api/ai/analyze` — Sandbox testing endpoint for arbitrary text
* `GET /api/export/csv` — Streams complete database records as a CSV download

---

## 🎯 Final Interview Discussion — Prepared Answers

*(Ref: Section 11 of Kiwi Connect Digital Assignment Specification)*

### 1. How does your AI workflow operate?
The workflow follows a 9-step automated pipeline:
1. Intake through Streamlit web form or FastAPI REST endpoint (`/api/enquiries`).
2. Duplicate detection evaluating phone, email, and token-level message overlap against past leads.
3. Prompt isolation and anti-injection sanitization.
4. Google Gemini 3.5 Flash Lite structured reasoning.
5. Strict classification into 1 of the 7 allowed Kiwi Connect Digital service categories.
6. Entity extraction of budget, location, urgency, key requirements, and missing info.
7. Multi-factor lead scoring (0–100) and priority assignment (`High`, `Medium`, `Low`).
8. Generation of suggested customer response, next steps, and follow-up timeline.
9. Atomic persistence to SQLite with real-time reflection across the CRM dashboard.

### 2. How does your AI extract structured information?
We leverage Gemini's native structured JSON mode (`response_mime_type: "application/json"`) paired with explicit schema definition in the system prompt. Extracted JSON is validated through a defensive normalization layer:
* Categories not in the allowed list are clamped to `Other Services`.
* Priorities outside `[High, Medium, Low]` default to `Medium`.
* Lead scores are constrained to integers `[0, 100]`.
* Missing values are mapped to explicit `null` or `Not specified` rather than hallucinated facts.

### 3. How do you handle incorrect AI responses?
We utilize a 3-tier defense:
1. **Schema Guardrails:** Automated validation ensures malformed outputs or hallucinated categories are corrected programmatically before database insertion.
2. **Human-in-the-Loop Admin Review:** The dashboard allows administrators to review, edit, and save responses before communicating with the customer.
3. **Resilient Heuristic Fallback Engine:** If an LLM call fails, times out, or encounters quota exhaustion, the system automatically falls back to deterministic rule-based NLP extraction, ensuring zero application crashes.

### 4. How would you handle 1,000 enquiries per day?
1,000 enquiries/day (~0.7 enquiries/min average, peaking at 15–20/min) is easily handled through:
1. **Database Upgrade:** Transition from SQLite to PostgreSQL with connection pooling (e.g. pgBouncer).
2. **Asynchronous Task Queue:** Decouple enquiry ingestion from LLM processing using Celery or Redis Queue (RQ); return an immediate `202 Accepted` to the client while worker processes execute the AI pipeline asynchronously.
3. **Horizontal Scaling:** Deploy FastAPI and Streamlit in stateless Docker containers orchestrated via Kubernetes or AWS ECS with auto-scaling.
4. **Rate Limiting:** Implement token-bucket throttling and exponential backoff retry policies for external API calls.

### 5. How would you reduce AI API costs?
1. **Model Selection:** Using `gemini-3.5-flash-lite` provides sub-second latency and costs less than 1/10th of frontier models while maintaining high extraction accuracy.
2. **Prompt Optimization:** Minimize prompt token overhead with concise schema definitions and few-shot examples.
3. **Semantic Caching:** Cache enquiry embeddings in Redis/ChromaDB so duplicate or highly similar queries retrieve previously computed analyses without invoking the LLM.
4. **Tiered Filtering:** Run lightweight regex and heuristic classifiers first; only dispatch complex, unstructured enquiries to the LLM.

### 6. How would you integrate this system with WhatsApp or a CRM?
* **WhatsApp:** Integrate with the **WhatsApp Business Cloud API** (via Meta Graph API or Twilio). Use webhooks to ingest inbound customer WhatsApp messages directly into the workflow, and trigger outbound approved template messages upon administrator approval.
* **CRM:** Expose bi-directional REST webhooks to push qualified leads with scores and categories into HubSpot, Zoho CRM, or Salesforce, and update lead statuses when deals close.

### 7. Which part of your project did you find most challenging?
Balancing high-precision extraction against real-world ambiguous customer input (e.g. informal Indian English, unstated budgets, or colloquial terms like *'Rs 50k'* vs *'₹50,000'* vs *'50 thousand'*) while guaranteeing 100% schema stability and zero runtime crashes, even in offline environments.

### 8. What improvements would you make if given another two days?
1. **Role-Based Authentication (RBAC):** Add JWT-based login with distinct roles (Admin, Sales Representative, Department Lead).
2. **Two-Way WhatsApp Webhook:** Complete automated conversational bot flow allowing customers to clarify missing details directly over WhatsApp.
3. **RAG Knowledge Base:** Implement vector search over Kiwi Connect Digital past case studies and pricing rate cards to generate dynamic pricing estimates.
4. **Automated Email Dispatcher:** Integrate SendGrid/SMTP to send emails directly upon admin approval.

---

## 🎬 2-3 Minute Demonstration Recording Script

For the video submission requirement:

1. **Introduction (0:00 – 0:30):**
   * State name and position applied for (*AI Intern at Kiwi Connect Digital*).
   * Briefly explain the problem: businesses waste hours manually reading and sorting customer leads.
   * Introduce LeadFlow AI.
2. **Live Enquiry Submission (0:30 – 1:15):**
   * Navigate to the **"Enquiry Intake Form"**.
   * Click the **"📍 Official Assignment Sample (Indore Store)"** preset.
   * Click **"Submit Enquiry & Run Automated AI Pipeline"**.
   * Show real-time extraction: Category (`E-commerce Development`), Budget (`₹50,000`), Location (`Indore`), Priority (`High`), Lead Score (`85/100`), Requirements, and Suggested Response.
3. **Lead Management CRM & Communication Tools (1:15 – 2:00):**
   * Switch to the **"Lead Management CRM"** tab.
   * Demonstrate real-time search and filtering.
   * Open the detailed Lead Inspector.
   * Highlight the **Duplicate Lead Alert** feature.
   * Edit the suggested response and click **"Save Edited Response"**.
   * Demonstrate the **1-Click WhatsApp Web** and **Email Draft** buttons.
4. **Executive Dashboard & REST API (2:00 – 2:45):**
   * Switch to the **"Executive Dashboard"** to show live KPIs, category distribution charts, and conversion progress.
   * Quickly open **`http://localhost:8000/docs`** to highlight the production FastAPI REST endpoints.
   * Conclude with system resilience (Gemini Flash + Heuristic offline fallback).

---

## 📄 License & Attribution

Developed for the **Kiwi Connect Digital AI Intern Technical Assignment**.  
Built with Python, Streamlit, FastAPI, Google GenAI, and SQLite.
