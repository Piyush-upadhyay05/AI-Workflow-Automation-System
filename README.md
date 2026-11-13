# AI-Powered Workflow Automation System

An AI-powered workflow automation system that analyzes, categorizes, and
prioritizes customer enquiries, extracts key requirements, generates
professional responses, and manages leads through an interactive admin
dashboard with database integration.

> **Project:** AI Intern -- Technical Assignment\
> **Organization:** Kiwi Connect Digital\
> **Status:** In development

## Overview

Businesses often spend considerable time manually reading customer
enquiries, identifying requirements, assigning categories, and preparing
replies. This project aims to automate that workflow using an AI model
and a web-based enquiry management dashboard.

Customers or administrators can submit an enquiry containing the
customer's name, phone number, email address, and message. The system
analyzes the message, extracts useful information, assigns a service
category and priority, suggests a customer response, and stores the
enquiry for administrators to review and manage.

## Objectives

-   Reduce repetitive manual work involved in processing customer
    enquiries.
-   Extract structured information from unstructured customer messages.
-   Categorize enquiries by the service requested.
-   Assign a Low, Medium, or High priority.
-   Generate suggested customer responses and follow-up questions.
-   Provide a dashboard for reviewing and managing enquiries.
-   Store enquiries and their AI-generated analysis for later retrieval.

## Planned Features

### 1. Enquiry Submission

A form for submitting: - Customer name - Phone number - Email address -
Enquiry message

### 2. AI-Powered Enquiry Analysis

The AI analysis is designed to identify: - Required service - Budget -
Customer location - Enquiry urgency - Important project requirements -
Missing information

### 3. Automatic Categorization

Enquiries will be classified into one of these categories: - Website
Development - Mobile Application Development - AI Software Development -
Digital Marketing - E-commerce Development - Custom Software
Development - Other Services

### 4. Priority Assignment

Each enquiry will be assigned a priority: - **Low** - **Medium** -
**High**

### 5. AI-Generated Customer Response

The system will suggest a professional response, recommended next steps,
and follow-up questions when information is missing. Administrators can
review and edit the suggested response. Sending messages automatically
is outside the assignment's required scope.

### 6. Admin Dashboard

The dashboard is intended to show: - Total enquiries - New enquiries -
High-priority enquiries - In-progress enquiries - Converted enquiries -
Category-wise enquiry distribution

Administrators will also be able to view enquiry details and AI
analysis, search and filter enquiries, and update enquiry status.

### 7. Database Management

The database will store customer enquiries, extracted information,
categories, priorities, suggested responses, and enquiry statuses.

## Technology Stack

The following stack is the proposed implementation. Update this section
if the final implementation uses different technologies.

  Component           Technology
  ------------------- ----------------------------------------------
  Frontend            React.js
  Styling             Tailwind CSS
  Backend             Python, FastAPI
  AI integration      Google Gemini API (or another supported LLM)
  Database            SQLite
  API communication   REST API
  Version control     Git and GitHub

## System Workflow

1.  A customer or administrator submits an enquiry.
2.  The frontend sends the enquiry to the backend API.
3.  The backend validates the submitted data.
4.  The AI model analyzes the enquiry message.
5.  The system extracts structured information and determines a category
    and priority.
6.  The AI generates a suggested response and follow-up questions, where
    needed.
7.  The enquiry and its analysis are saved in the database.
8.  The administrator reviews the result in the dashboard and updates
    the enquiry status.

## Proposed Project Structure

``` text
ai-workflow-automation/
├── frontend/             # React application
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py       # API entry point
│   │   ├── routes/       # API routes
│   │   ├── services/     # AI and workflow logic
│   │   ├── models/       # Database models
│   │   └── schemas/      # Request/response schemas
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

This is a suggested structure; adapt it to match the actual repository
as development progresses.

## Getting Started

The following setup is a starting point for the proposed stack. Commands
and files may need adjustment as the application is implemented.

### Prerequisites

-   Python 3.10 or later
-   Node.js and npm
-   Git
-   An API key for the selected AI provider, if using a hosted model

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-workflow-automation
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository URL.

### 2. Set up the backend

``` bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

**Windows (Command Prompt):**

``` bat
.venv\Scripts\activate
```

**Windows (PowerShell):**

``` powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

``` bash
source .venv/bin/activate
```

Install dependencies once `requirements.txt` has been created:

``` bash
pip install -r requirements.txt
```

Configure the required environment variables using the project's
`.env.example` as a guide. Start the server with the command appropriate
to the implemented FastAPI entry point. For example, if the entry point
is `app.main:app`:

``` bash
uvicorn app.main:app --reload
```

The API documentation is normally available at
`http://127.0.0.1:8000/docs` when the server is running.

### 3. Set up the frontend

Open a second terminal:

``` bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by the frontend development server.

> The backend and frontend setup instructions should be verified against
> the final source code before submission.

## Environment Variables and API Key Safety

Keep secrets in a local `.env` file and never commit that file to
GitHub. For example, the backend may use a variable such as:

``` env
GEMINI_API_KEY=your_api_key_here
```

Use the exact variable name required by your implementation. Add `.env`
to `.gitignore`, and provide a `.env.example` containing placeholder
values only. Never put a private AI API key in frontend code or expose
it in a public repository.

## API Design (Planned)

The exact endpoints should match the implemented backend. A possible
initial design is:

  Method    Endpoint                       Purpose
  --------- ------------------------------ -------------------------------
  `POST`    `/api/enquiries`               Create and analyze an enquiry
  `GET`     `/api/enquiries`               List enquiries
  `GET`     `/api/enquiries/{id}`          Retrieve one enquiry
  `PATCH`   `/api/enquiries/{id}/status`   Update enquiry status
  `GET`     `/api/dashboard/stats`         Retrieve dashboard statistics

These are proposed endpoints, not a claim that they are already
implemented.

## Data and Reliability Considerations

-   Use sample customer data for development and demonstrations.
-   Validate submitted fields on the backend.
-   Treat AI output as a suggestion and validate its structure before
    saving it.
-   Handle missing, malformed, or failed AI responses gracefully.
-   Allow administrators to review AI-generated content before using it.
-   Keep API keys and other credentials private.

## Testing

As features are implemented, test: - Enquiry form validation - AI
extraction and category assignment - Priority assignment - Response
generation - Database creation and retrieval - Search, filtering, and
status updates - Error handling when the AI provider is unavailable

Use sample data only; do not include real customer information in
demonstrations or the repository.

## Bonus Features

Potential enhancements after the core workflow is working: - Duplicate
enquiry detection - AI-based lead scoring - Follow-up reminder
suggestions - Email or WhatsApp integration - Analytics and reporting -
Automatic assignment to team members - CSV or Excel export -
AI-generated enquiry summaries

## Demo and Submission Checklist

Before submitting the assignment, add or verify: - \[ \] Working
application and tested setup instructions - \[ \] Complete source code
in this repository - \[ \] Database schema or structure - \[ \]
Explanation of the AI model used - \[ \] Workflow and system
architecture explanation - \[ \] A 2--3 minute screen-recorded
demonstration - \[ \] Screenshots or a demo link, if available - \[ \]
Any third-party libraries and tools used

## Limitations and Future Improvements

The quality of extraction and generated responses depends on the
selected AI model and the quality of the input message. Future
improvements could include stronger output validation, more detailed
analytics, CRM integrations, rate limiting, authentication, and support
for higher enquiry volumes.

## Acknowledgements

Developed as an AI Intern technical assignment for **Kiwi Connect
Digital**. The project focuses on practical AI integration, workflow
automation, API development, database management, and enquiry
operations.

------------------------------------------------------------------------

**Note:** This README describes the intended project and proposed setup.
Update the feature status, technology stack, folder structure, commands,
and API endpoints to reflect what is actually implemented before final
submission.
