"""
Sample Data Seeder for Kiwi Connect Digital - AI Workflow Automation System.
Populates realistic customer enquiries across multiple business verticals, budgets,
locations, priorities, and test cases (including duplicate detection).
"""

import database
import ai_engine

SAMPLE_LEADS = [
    {
        "customer_name": "Rajesh Gupta",
        "phone": "+91 98260 12345",
        "email": "rajesh.gupta@indorestyles.in",
        "message": "I own a clothing store in Indore. I need an e-commerce website where customers can browse products, place orders and make online payments. My budget is around ₹50,000.",
        "status": "In Progress"
    },
    {
        "customer_name": "Dr. Sunita Deshmukh",
        "phone": "+91 98111 87654",
        "email": "sunita@apollohealthtech.org",
        "message": "We need an urgent AI-powered triage chatbot and patient records analysis system for our multi-specialty hospital in Pune. Must be HIPAA compliant and ready within 3 weeks. Budget is ₹4,50,000. Please contact immediately.",
        "status": "New"
    },
    {
        "customer_name": "Karthik Raja",
        "phone": "+91 97400 55432",
        "email": "karthik@hyperlocalnow.com",
        "message": "Looking for iOS and Android flutter app development for a 15-minute grocery delivery startup in Bangalore. Need real-time rider tracking, inventory management, and UPI payment. Budget is ₹2,00,000 - ₹2,50,000 with launch target in 2 months.",
        "status": "Converted"
    },
    {
        "customer_name": "Neha Kapur",
        "phone": "+91 99201 33456",
        "email": "neha@kapurfintech.in",
        "message": "We are a B2B SaaS startup in Mumbai looking for a complete digital marketing agency partner for performance marketing, SEO, LinkedIn lead generation, and content creation. Monthly retainer budget is ₹60,000/month.",
        "status": "In Progress"
    },
    {
        "customer_name": "Vikram Rathore",
        "phone": "+91 94140 98765",
        "email": "vikram@rathorelogistics.com",
        "message": "Need a custom cloud ERP and fleet management portal with GPS tracking for our 120 logistics trucks across Rajasthan and Gujarat. Budget is ₹6,00,000. Completion desired within 90 days.",
        "status": "New"
    },
    {
        "customer_name": "Rajesh Gupta (Duplicate Test)",
        "phone": "+91 98260 12345",
        "email": "rajesh.gupta@indorestyles.in",
        "message": "Hello, following up on my previous query for the clothing store e-commerce website in Indore with ₹50,000 budget. Need online payment gateway setup.",
        "status": "New"
    }
]


def seed_database(clear_existing: bool = False):
    """Seed sample enquiries and run AI analysis on each."""
    database.init_db()

    if clear_existing:
        with database.get_connection() as conn:
            conn.execute("DELETE FROM enquiries")

    created_ids = []
    for lead in SAMPLE_LEADS:
        # Check duplicate first
        is_dup, dup_id, dup_reason = database.check_duplicate(
            customer_name=lead["customer_name"],
            phone=lead["phone"],
            email=lead["email"],
            message=lead["message"]
        )

        enquiry_id = database.add_enquiry(
            customer_name=lead["customer_name"],
            phone=lead["phone"],
            email=lead["email"],
            message=lead["message"]
        )

        # Run heuristic or AI analysis for seed data
        analysis = ai_engine.analyze_enquiry_heuristic(lead["message"])

        # Save analysis
        database.save_ai_analysis(
            enquiry_id=enquiry_id,
            analysis=analysis,
            is_duplicate=is_dup,
            duplicate_of_id=dup_id
        )

        # Set status
        database.update_status(enquiry_id, lead["status"])
        created_ids.append(enquiry_id)

    print(f"Successfully seeded {len(created_ids)} customer enquiries! IDs: {created_ids}")
    return created_ids


if __name__ == "__main__":
    seed_database(clear_existing=False)
