"""
Comprehensive Automated Test Suite for Kiwi Connect Digital - AI Workflow Automation System.
Verifies database integrity, AI parsing, duplicate detection, and FastAPI REST endpoints.
"""

import os
import sys
import unittest
from pathlib import Path

# Ensure root directory is on PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
import database
import ai_engine
from fastapi.testclient import TestClient
import api


class TestAIWorkflowAutomation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.init_db()
        cls.client = TestClient(api.app)

    def test_01_database_schema(self):
        """Verify all required columns exist in SQLite schema."""
        with database.get_connection() as conn:
            cursor = conn.execute("PRAGMA table_info(enquiries)")
            cols = {row["name"] for row in cursor.fetchall()}

        required = [
            "id", "customer_name", "phone", "email", "message",
            "category", "priority", "status", "budget", "location",
            "urgency", "lead_score", "lead_score_reason", "summary",
            "assigned_to", "is_duplicate", "duplicate_of_id",
            "follow_up_date", "follow_up_action", "tags",
            "ai_analysis", "ai_response", "edited_response",
            "created_at", "updated_at"
        ]
        for col in required:
            self.assertIn(col, cols, f"Column '{col}' must exist in enquiries table")

    def test_02_add_and_retrieve_enquiry(self):
        """Test inserting a new enquiry and retrieving it."""
        enquiry_id = database.add_enquiry(
            customer_name="Test Customer",
            phone="+91 99999 11111",
            email="test@customer.com",
            message="Need a simple 5-page business portfolio website. Budget is ₹25,000."
        )
        self.assertGreater(enquiry_id, 0)

        record = database.get_enquiry_by_id(enquiry_id)
        self.assertIsNotNone(record)
        self.assertEqual(record["customer_name"], "Test Customer")
        self.assertEqual(record["status"], "New")

    def test_03_heuristic_ai_extraction(self):
        """Test offline heuristic engine extraction on the Indore example."""
        message = (
            "I own a clothing store in Indore. I need an e-commerce website where "
            "customers can browse products, place orders and make online payments. "
            "My budget is around ₹50,000."
        )
        analysis = ai_engine.analyze_enquiry_heuristic(message)

        self.assertEqual(analysis["category"], "E-commerce Development")
        self.assertEqual(analysis["location"], "Indore")
        self.assertIsNotNone(analysis["budget"])
        self.assertIn("50,000", analysis["budget"])
        self.assertGreaterEqual(analysis["lead_score"], 70)
        self.assertTrue(len(analysis["requirements"]) > 0)
        self.assertIn("suggested_response", analysis)

    def test_04_duplicate_detection(self):
        """Verify duplicate detection by phone, email, and similarity."""
        import time
        unique_phone = f"+91 91{int(time.time()) % 100000000:08d}"
        unique_email = f"lead_{int(time.time())}@example.com"

        # Insert base lead
        base_id = database.add_enquiry(
            customer_name="Original Lead",
            phone=unique_phone,
            email=unique_email,
            message="Looking for mobile app development for restaurant delivery."
        )

        # Exact phone duplicate
        is_dup, dup_id, reason = database.check_duplicate(
            customer_name="Different Name",
            phone=unique_phone,
            email="other_unique@example.com",
            message="Query about app."
        )
        self.assertTrue(is_dup)
        self.assertEqual(dup_id, base_id)
        self.assertIn("phone", reason.lower())

        # Exact email duplicate
        is_dup_mail, dup_id_mail, _ = database.check_duplicate(
            customer_name="Another Name",
            phone="+91 90000 99999",
            email=unique_email,
            message="Another question."
        )
        self.assertTrue(is_dup_mail)
        self.assertEqual(dup_id_mail, base_id)

    def test_05_update_status_and_response(self):
        """Test status transitions and response editing."""
        enquiry_id = database.add_enquiry(
            customer_name="Status Test",
            phone="+91 90000 00001",
            email="status@test.com",
            message="Test status update message."
        )

        # Update status
        database.update_status(enquiry_id, "In Progress")
        rec = database.get_enquiry_by_id(enquiry_id)
        self.assertEqual(rec["status"], "In Progress")

        # Edit response
        custom_reply = "Customized message from administrator."
        database.update_edited_response(enquiry_id, custom_reply)
        rec = database.get_enquiry_by_id(enquiry_id)
        self.assertEqual(rec["edited_response"], custom_reply)

    def test_06_fastapi_endpoints(self):
        """Test FastAPI REST API handlers directly without requiring socket binding."""
        # 1. Health check
        res_root = api.root()
        self.assertEqual(res_root["status"], "healthy")
        self.assertIn("Kiwi Connect Digital", res_root["company"])

        # 2. List enquiries
        res_list = api.list_enquiries()
        self.assertIsInstance(res_list, list)

        # 3. Analytics stats
        res_stats = api.get_dashboard_statistics()
        self.assertIn("total", res_stats)
        self.assertIn("conversion_rate", res_stats)
        self.assertIn("category_counts", res_stats)

        # 4. Submit enquiry through API handler
        payload = api.EnquiryCreate(
            customer_name="API Direct User",
            phone="+91 98888 77777",
            email="api.direct@test.org",
            message="We need custom AI software development for automated medical billing. Budget is ₹3,00,000."
        )
        res_submit = api.submit_enquiry(payload)
        self.assertIn("enquiry", res_submit)
        enq = res_submit["enquiry"]
        self.assertEqual(enq["customer_name"], "API Direct User")
        self.assertIn(enq["category"], config.CATEGORIES)

        # 5. Status update handler
        status_payload = api.StatusUpdate(status="In Progress")
        res_status = api.update_enquiry_status(enq["id"], status_payload)
        self.assertEqual(res_status["new_status"], "In Progress")

        # 6. Response edit handler
        resp_payload = api.ResponseUpdate(response_text="Approved response from admin.")
        res_resp = api.edit_suggested_response(enq["id"], resp_payload)
        self.assertEqual(res_resp["edited_response"], "Approved response from admin.")


if __name__ == "__main__":
    unittest.main()
