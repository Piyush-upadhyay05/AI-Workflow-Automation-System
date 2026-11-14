"""
FastAPI REST API for Kiwi Connect Digital - AI Workflow Automation System.
Provides production-ready RESTful endpoints for enquiry submission, AI workflow
execution, lead status management, analytics, and data export.
"""

import io
import csv
import json
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

import config
import database
import ai_engine

# Initialize Database
database.init_db()

app = FastAPI(
    title=f"{config.COMPANY_NAME} — LeadFlow Automation API",
    description="Enterprise REST API for AI-powered customer enquiry ingestion, analysis, scoring, and CRM management.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-platform integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# Pydantic Request / Response Models
# -------------------------------------------------------------

class EnquiryCreate(BaseModel):
    customer_name: str = Field(..., example="Rajesh Gupta")
    phone: Optional[str] = Field(None, example="+91 98260 12345")
    email: Optional[str] = Field(None, example="rajesh.gupta@indorestyles.in")
    message: str = Field(..., example="I own a clothing store in Indore. I need an e-commerce website where customers can browse products, place orders and make online payments. My budget is around ₹50,000.")


class StatusUpdate(BaseModel):
    status: str = Field(..., example="In Progress")


class ResponseUpdate(BaseModel):
    response_text: str = Field(..., example="Custom edited response for customer...")


class AssignmentUpdate(BaseModel):
    assigned_to: str = Field(..., example="Rahul Sharma (E-Commerce Specialist)")


class DirectAnalyzeRequest(BaseModel):
    message: str = Field(..., example="Need a mobile delivery app in Bangalore with budget ₹2 Lakh.")


# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------

@app.get("/", tags=["System"])
def root():
    """System health and metadata endpoint."""
    return {
        "company": config.COMPANY_NAME,
        "tagline": config.COMPANY_TAGLINE,
        "system": config.APP_TITLE,
        "status": "healthy",
        "api_docs": "/docs",
        "models_available": [config.DEFAULT_MODEL] + config.FALLBACK_MODELS
    }


@app.post("/api/enquiries", status_code=status.HTTP_201_CREATED, tags=["Enquiries"])
def submit_enquiry(enquiry: EnquiryCreate):
    """
    Core Automated Workflow:
    Step 1: Receive customer enquiry.
    Step 2: Check for duplicate submissions.
    Step 3: AI analyzes customer message & extracts structured attributes.
    Step 4: Automatic Categorization & Lead Scoring.
    Step 5: Generate suggested response & next steps.
    Step 6: Persist everything in SQLite database.
    """
    if not enquiry.customer_name.strip() or not enquiry.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Customer name and enquiry message are strictly required."
        )

    # 1. Duplicate Detection
    is_dup, dup_id, dup_reason = database.check_duplicate(
        customer_name=enquiry.customer_name,
        phone=enquiry.phone,
        email=enquiry.email,
        message=enquiry.message
    )

    # 2. Persist Enquiry Record
    enquiry_id = database.add_enquiry(
        customer_name=enquiry.customer_name,
        phone=enquiry.phone,
        email=enquiry.email,
        message=enquiry.message
    )

    # 3. AI Extraction & Analysis Pipeline
    analysis = ai_engine.analyze_enquiry(enquiry.message)

    # 4. Save Structured AI Output
    database.save_ai_analysis(
        enquiry_id=enquiry_id,
        analysis=analysis,
        is_duplicate=is_dup,
        duplicate_of_id=dup_id
    )

    created = database.get_enquiry_by_id(enquiry_id)
    return {
        "message": "Enquiry submitted and analyzed successfully.",
        "enquiry": created,
        "duplicate_detection": {
            "is_duplicate": is_dup,
            "duplicate_of_id": dup_id,
            "reason": dup_reason
        }
    }


@app.get("/api/enquiries", tags=["Enquiries"])
def list_enquiries(
    search: Optional[str] = Query(None, description="Search term for name, email, phone, message"),
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by priority (High, Medium, Low)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status")
):
    """Retrieve filtered enquiries."""
    return database.get_all_enquiries(
        search=search,
        category=category,
        priority=priority,
        status=status_filter
    )


@app.delete("/api/enquiries", tags=["Enquiries"])
def clear_all_enquiries():
    """Clear all customer enquiries from the database and reset sequence."""
    deleted_count = database.delete_all_enquiries()
    return {
        "message": f"Successfully deleted {deleted_count} enquiries from database.",
        "deleted_count": deleted_count
    }


@app.get("/api/enquiries/{enquiry_id}", tags=["Enquiries"])
def get_enquiry(enquiry_id: int):
    """Retrieve details and AI analysis for a specific enquiry."""
    enquiry = database.get_enquiry_by_id(enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    if enquiry.get("ai_analysis"):
        try:
            enquiry["parsed_analysis"] = json.loads(enquiry["ai_analysis"])
        except Exception:
            enquiry["parsed_analysis"] = None

    return enquiry


@app.patch("/api/enquiries/{enquiry_id}/status", tags=["Workflow"])
def update_enquiry_status(enquiry_id: int, payload: StatusUpdate):
    """Update lead status (New, In Progress, Converted, Closed)."""
    if payload.status not in config.STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {config.STATUSES}")

    enquiry = database.get_enquiry_by_id(enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    database.update_status(enquiry_id, payload.status)
    return {"message": "Status updated successfully", "new_status": payload.status}


@app.patch("/api/enquiries/{enquiry_id}/response", tags=["Workflow"])
def edit_suggested_response(enquiry_id: int, payload: ResponseUpdate):
    """Allow administrator to review, edit, and save customer response."""
    enquiry = database.get_enquiry_by_id(enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    database.update_edited_response(enquiry_id, payload.response_text)
    return {"message": "Response updated successfully", "edited_response": payload.response_text}


@app.patch("/api/enquiries/{enquiry_id}/assign", tags=["Workflow"])
def assign_team_member(enquiry_id: int, payload: AssignmentUpdate):
    """Manually reassign enquiry to a specific team member."""
    enquiry = database.get_enquiry_by_id(enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    database.update_assignment(enquiry_id, payload.assigned_to)
    return {"message": "Team assignment updated successfully", "assigned_to": payload.assigned_to}


@app.post("/api/enquiries/{enquiry_id}/reanalyze", tags=["AI Workflow"])
def reanalyze_enquiry(enquiry_id: int):
    """Re-run AI analysis on an existing customer enquiry."""
    enquiry = database.get_enquiry_by_id(enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    analysis = ai_engine.analyze_enquiry(enquiry["message"])

    is_dup, dup_id, _ = database.check_duplicate(
        customer_name=enquiry["customer_name"],
        phone=enquiry.get("phone"),
        email=enquiry.get("email"),
        message=enquiry["message"],
        exclude_id=enquiry_id
    )

    database.save_ai_analysis(
        enquiry_id=enquiry_id,
        analysis=analysis,
        is_duplicate=is_dup,
        duplicate_of_id=dup_id
    )

    return {
        "message": "AI analysis re-executed and saved.",
        "analysis": analysis
    }


@app.get("/api/dashboard/stats", tags=["Analytics"])
def get_dashboard_statistics():
    """Retrieve aggregated dashboard metrics, conversion rate, and distributions."""
    return database.get_analytics_summary()


@app.post("/api/ai/analyze", tags=["AI Lab"])
def direct_ai_analysis(payload: DirectAnalyzeRequest):
    """Direct AI analysis endpoint for sandbox testing without saving to database."""
    return ai_engine.analyze_enquiry(payload.message)


@app.get("/api/export/csv", tags=["Export"])
def export_csv():
    """Export all enquiries to CSV format."""
    enquiries = database.get_all_enquiries()
    output = io.StringIO()
    writer = csv.writer(output)

    headers = [
        "ID", "Customer Name", "Phone", "Email", "Category", "Priority",
        "Urgency", "Budget", "Location", "Lead Score", "Status", "Assigned To",
        "Is Duplicate", "Created At"
    ]
    writer.writerow(headers)

    for e in enquiries:
        writer.writerow([
            e.get("id"),
            e.get("customer_name"),
            e.get("phone"),
            e.get("email"),
            e.get("category"),
            e.get("priority"),
            e.get("urgency"),
            e.get("budget"),
            e.get("location"),
            e.get("lead_score"),
            e.get("status"),
            e.get("assigned_to"),
            "Yes" if e.get("is_duplicate") else "No",
            e.get("created_at")
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=enquiries_export.csv"}
    )
