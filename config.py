"""
Configuration and constants for Kiwi Connect Digital - AI Workflow Automation System.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "enquiries.db"

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash"
]

# Branding & System Identity
COMPANY_NAME = "Kiwi Connect Digital"
COMPANY_TAGLINE = "Think Social. Think Kiwi. | Build Smart. Automate Better. Think Beyond."
APP_TITLE = "LeadFlow AI — Intelligent Workflow Automation"
APP_SUBTITLE = "AI Intern Technical Assignment | Kiwi Connect Digital"

# Assignment Allowed Categories (Strict requirement from section 3.C)
CATEGORIES = [
    "Website Development",
    "Mobile Application Development",
    "AI Software Development",
    "Digital Marketing",
    "E-commerce Development",
    "Custom Software Development",
    "Other Services",
]

# Enquiry Workflow Statuses
STATUSES = ["New", "In Progress", "Converted", "Closed"]

# Priority Levels (Strict requirement from section 3.B / 4.Step 6)
PRIORITIES = ["High", "Medium", "Low"]

# Urgency Levels
URGENCIES = ["High", "Medium", "Low", "Unknown"]

# Lead Scoring Tiers
LEAD_TIERS = {
    "Hot": (80, 100),
    "Warm": (50, 79),
    "Cold": (0, 49)
}

# Automatic Department / Team Member Assignment Routing (Bonus feature 8)
TEAM_ROUTING = {
    "E-commerce Development": "Rahul Sharma (E-Commerce Specialist - Indore Hub)",
    "Website Development": "Amit Verma (Senior Web Solutions Lead)",
    "Mobile Application Development": "Sneha Roy (Mobile Platforms Lead)",
    "AI Software Development": "Dr. Priya Patel (AI/ML Solutions Architect)",
    "Digital Marketing": "Vikram Malhotra (Growth & Digital Marketing Lead)",
    "Custom Software Development": "Karan Mehra (Custom Enterprise Systems Lead)",
    "Other Services": "Pooja Nair (Client Relations & General Tech Lead)"
}

# Pre-configured Sample Enquiries for Quick Demonstration
SAMPLE_PRESETS = [
    {
        "title": "📍 Official Assignment Sample (Indore Store)",
        "name": "Rajesh Gupta",
        "phone": "+91 98260 12345",
        "email": "rajesh.gupta@indorestyles.in",
        "message": "I own a clothing store in Indore. I need an e-commerce website where customers can browse products, place orders and make online payments. My budget is around ₹50,000."
    },
    {
        "title": "🚨 Urgent Healthcare AI Solution (High Priority)",
        "name": "Dr. Sunita Deshmukh",
        "phone": "+91 98111 87654",
        "email": "sunita@apollohealthtech.org",
        "message": "We need an urgent AI-powered triage chatbot and patient records analysis system for our multi-specialty hospital in Pune. Must be HIPAA compliant and ready within 3 weeks. Budget is ₹4,50,000. Please contact immediately."
    },
    {
        "title": "📱 Quick Delivery Mobile App (Bangalore)",
        "name": "Karthik Raja",
        "phone": "+91 97400 55432",
        "email": "karthik@hyperlocalnow.com",
        "message": "Looking for iOS and Android flutter app development for a 15-minute grocery delivery startup in Bangalore. Need real-time rider tracking, inventory management, and UPI payment. Budget is ₹2,00,000 - ₹2,50,000 with launch target in 2 months."
    },
    {
        "title": "📈 Organic Growth & SEO Marketing (Mumbai)",
        "name": "Neha Kapur",
        "phone": "+91 99201 33456",
        "email": "neha@kapurfintech.in",
        "message": "We are a B2B SaaS startup in Mumbai looking for a complete digital marketing agency partner for performance marketing, SEO, LinkedIn lead generation, and content creation. Monthly retainer budget is ₹60,000/month."
    },
    {
        "title": "⚠️ Ambiguous Lead / Missing Information (Low Priority)",
        "name": "Anonymous User",
        "phone": "",
        "email": "visitor@yahoo.com",
        "message": "Can you make software for my shop? How much does it cost?"
    }
]
