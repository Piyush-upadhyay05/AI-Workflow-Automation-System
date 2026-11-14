"""
Database management module for Kiwi Connect Digital - AI Workflow Automation System.
Handles SQLite connection, automated schema migrations, CRUD operations,
duplicate detection, and aggregated analytics reporting.
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple
from config import DB_PATH, STATUSES, TEAM_ROUTING


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables, run schema migrations, and build indexes."""
    with get_connection() as conn:
        # Base table creation
        conn.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                message TEXT NOT NULL,
                category TEXT DEFAULT 'Unclassified',
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'New',
                ai_analysis TEXT,
                ai_response TEXT,
                budget TEXT,
                location TEXT,
                urgency TEXT DEFAULT 'Unknown',
                lead_score INTEGER DEFAULT 50,
                lead_score_reason TEXT,
                summary TEXT,
                assigned_to TEXT,
                is_duplicate INTEGER DEFAULT 0,
                duplicate_of_id INTEGER,
                follow_up_date TEXT,
                follow_up_action TEXT,
                tags TEXT,
                edited_response TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Dynamic schema migration for existing databases
        cursor = conn.execute("PRAGMA table_info(enquiries)")
        existing_cols = {row["name"] for row in cursor.fetchall()}

        schema_additions = {
            "budget": "TEXT",
            "location": "TEXT",
            "urgency": "TEXT DEFAULT 'Unknown'",
            "lead_score": "INTEGER DEFAULT 50",
            "lead_score_reason": "TEXT",
            "summary": "TEXT",
            "assigned_to": "TEXT",
            "is_duplicate": "INTEGER DEFAULT 0",
            "duplicate_of_id": "INTEGER",
            "follow_up_date": "TEXT",
            "follow_up_action": "TEXT",
            "tags": "TEXT",
            "edited_response": "TEXT",
            "updated_at": "TEXT DEFAULT CURRENT_TIMESTAMP"
        }

        for col, col_type in schema_additions.items():
            if col not in existing_cols:
                conn.execute(f"ALTER TABLE enquiries ADD COLUMN {col} {col_type}")

        # Performance indexes for search and dashboard analytics
        conn.execute("CREATE INDEX IF NOT EXISTS idx_enquiries_status ON enquiries(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_enquiries_category ON enquiries(category)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_enquiries_priority ON enquiries(priority)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_enquiries_created ON enquiries(created_at)")


def _clean_str(val: Optional[str]) -> str:
    return (val or "").strip().lower()


def _text_similarity(s1: str, s2: str) -> float:
    """Calculate token-level Jaccard similarity between two messages."""
    w1 = set(_clean_str(s1).split())
    w2 = set(_clean_str(s2).split())
    if not w1 or not w2:
        return 0.0
    intersection = len(w1.intersection(w2))
    union = len(w1.union(w2))
    return intersection / union if union > 0 else 0.0


def check_duplicate(
    customer_name: str,
    phone: Optional[str],
    email: Optional[str],
    message: str,
    exclude_id: Optional[int] = None
) -> Tuple[bool, Optional[int], str]:
    """
    Bonus Feature 1: Automatic duplicate enquiry detection.
    Evaluates existing enquiries against phone, email, or message content.
    Returns (is_duplicate, original_enquiry_id, reason).
    """
    clean_phone = "".join(filter(str.isdigit, phone or ""))
    clean_email = _clean_str(email)
    clean_msg = _clean_str(message)

    with get_connection() as conn:
        query = "SELECT id, customer_name, phone, email, message FROM enquiries"
        params = []
        if exclude_id:
            query += " WHERE id != ?"
            params.append(exclude_id)
        query += " ORDER BY id ASC"

        rows = conn.execute(query, params).fetchall()

        for row in rows:
            row_id = row["id"]
            row_phone = "".join(filter(str.isdigit, row["phone"] or ""))
            row_email = _clean_str(row["email"])
            row_msg = _clean_str(row["message"])

            # 1. Exact phone match (if > 7 digits)
            if clean_phone and len(clean_phone) >= 8 and clean_phone == row_phone:
                return (True, row_id, f"Duplicate phone number matched with Enquiry #{row_id}")

            # 2. Exact email match (if valid format)
            if clean_email and "@" in clean_email and clean_email == row_email:
                return (True, row_id, f"Duplicate email address matched with Enquiry #{row_id}")

            # 3. High textual similarity in message (> 80% word overlap)
            if len(clean_msg) > 20 and _text_similarity(clean_msg, row_msg) >= 0.80:
                return (True, row_id, f"High message content similarity matched with Enquiry #{row_id}")

    return (False, None, "")


def add_enquiry(
    customer_name: str,
    phone: Optional[str],
    email: Optional[str],
    message: str
) -> int:
    """Store customer enquiry record in the database."""
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO enquiries (
                customer_name, phone, email, message, status, updated_at
            )
            VALUES (?, ?, ?, ?, 'New', CURRENT_TIMESTAMP)
        """, (customer_name.strip(), (phone or "").strip(), (email or "").strip(), message.strip()))
        return cursor.lastrowid


def save_ai_analysis(
    enquiry_id: int,
    analysis: Dict[str, Any],
    is_duplicate: bool = False,
    duplicate_of_id: Optional[int] = None
) -> None:
    """Update enquiry with full AI analysis extraction, scoring, and workflow fields."""
    category = analysis.get("category", "Other Services")
    assigned_to = TEAM_ROUTING.get(category, "General Technical Support")

    tags_json = json.dumps(analysis.get("requirements", []), ensure_ascii=False)
    ai_analysis_json = json.dumps(analysis, ensure_ascii=False)

    with get_connection() as conn:
        conn.execute("""
            UPDATE enquiries
            SET category = ?,
                priority = ?,
                budget = ?,
                location = ?,
                urgency = ?,
                lead_score = ?,
                lead_score_reason = ?,
                summary = ?,
                assigned_to = ?,
                is_duplicate = ?,
                duplicate_of_id = ?,
                follow_up_date = ?,
                follow_up_action = ?,
                tags = ?,
                ai_analysis = ?,
                ai_response = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            category,
            analysis.get("priority", "Medium"),
            analysis.get("budget"),
            analysis.get("location"),
            analysis.get("urgency", "Unknown"),
            analysis.get("lead_score", 50),
            analysis.get("lead_score_reason", ""),
            analysis.get("summary", ""),
            assigned_to,
            1 if is_duplicate else 0,
            duplicate_of_id,
            analysis.get("follow_up_date", "Within 48 hours"),
            analysis.get("follow_up_action", "Initial requirement consultation"),
            tags_json,
            ai_analysis_json,
            analysis.get("suggested_response", ""),
            enquiry_id
        ))


def get_all_enquiries(
    search: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve enquiries with optional search query and multi-attribute filters."""
    query = "SELECT * FROM enquiries WHERE 1=1"
    params: List[Any] = []

    if isinstance(search, str) and search.strip():
        term = f"%{search.strip()}%"
        query += " AND (customer_name LIKE ? OR email LIKE ? OR phone LIKE ? OR message LIKE ? OR summary LIKE ?)"
        params.extend([term, term, term, term, term])

    if isinstance(category, str) and category != "All":
        query += " AND category = ?"
        params.append(category)

    if isinstance(priority, str) and priority != "All":
        query += " AND priority = ?"
        params.append(priority)

    if isinstance(status, str) and status != "All":
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY created_at DESC, id DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def get_enquiry_by_id(enquiry_id: int) -> Optional[Dict[str, Any]]:
    """Fetch complete details of a specific enquiry."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM enquiries WHERE id = ?", (enquiry_id,)).fetchone()
        return dict(row) if row else None


def update_status(enquiry_id: int, new_status: str) -> None:
    """Update workflow status of an enquiry."""
    if new_status not in STATUSES:
        raise ValueError(f"Invalid enquiry status: {new_status}. Allowed: {STATUSES}")

    with get_connection() as conn:
        conn.execute("""
            UPDATE enquiries
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_status, enquiry_id))


def update_edited_response(enquiry_id: int, response_text: str) -> None:
    """Save an administrator-reviewed / edited customer response."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE enquiries
            SET edited_response = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (response_text.strip(), enquiry_id))


def update_assignment(enquiry_id: int, assigned_to: str) -> None:
    """Manually reassign enquiry to a specific team member."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE enquiries
            SET assigned_to = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (assigned_to.strip(), enquiry_id))


def delete_enquiry(enquiry_id: int) -> bool:
    """Remove an enquiry from the database."""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM enquiries WHERE id = ?", (enquiry_id,))
        return cursor.rowcount > 0


def delete_all_enquiries() -> int:
    """Remove all enquiries from the database and reset the ID sequence to 1."""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM enquiries")
        count = cursor.rowcount
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'enquiries'")
        return count


def get_analytics_summary() -> Dict[str, Any]:
    """Calculate aggregated metrics and distributions for the Admin Dashboard."""
    enquiries = get_all_enquiries()
    total = len(enquiries)

    new_count = sum(1 for e in enquiries if e.get("status") == "New")
    in_progress = sum(1 for e in enquiries if e.get("status") == "In Progress")
    converted = sum(1 for e in enquiries if e.get("status") == "Converted")
    closed = sum(1 for e in enquiries if e.get("status") == "Closed")
    high_priority = sum(1 for e in enquiries if e.get("priority") == "High")
    duplicates = sum(1 for e in enquiries if e.get("is_duplicate") == 1)

    conversion_rate = (converted / total * 100) if total > 0 else 0.0

    scores = [e.get("lead_score") for e in enquiries if e.get("lead_score") is not None]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    # Categorical distributions
    category_counts: Dict[str, int] = {}
    for e in enquiries:
        cat = e.get("category") or "Unclassified"
        category_counts[cat] = category_counts.get(cat, 0) + 1

    priority_counts: Dict[str, int] = {"High": 0, "Medium": 0, "Low": 0}
    for e in enquiries:
        pri = e.get("priority") or "Medium"
        priority_counts[pri] = priority_counts.get(pri, 0) + 1

    status_counts: Dict[str, int] = {s: 0 for s in STATUSES}
    for e in enquiries:
        st = e.get("status") or "New"
        status_counts[st] = status_counts.get(st, 0) + 1

    return {
        "total": total,
        "new": new_count,
        "in_progress": in_progress,
        "converted": converted,
        "closed": closed,
        "high_priority": high_priority,
        "duplicates": duplicates,
        "conversion_rate": round(conversion_rate, 1),
        "avg_lead_score": avg_score,
        "category_counts": category_counts,
        "priority_counts": priority_counts,
        "status_counts": status_counts,
    }
