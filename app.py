"""
Kiwi Connect Digital — AI Workflow Automation System
Professional Admin Dashboard & Customer Intake Portal.
Evaluated for AI Intern Technical Assignment.
"""

import io
import json
import urllib.parse
import pandas as pd
import streamlit as st

import config
import database
import ai_engine

# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title=f"{config.APP_TITLE}",
    page_icon="🥝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database Schema & Migrations
database.init_db()

# -------------------- CUSTOM CSS STYLING --------------------

st.markdown("""
<style>
    /* Global Kiwi Connect Digital branding */
    .kiwi-header {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2b4a 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        border-left: 6px solid #10b981;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .kiwi-header h1 {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        padding-bottom: 4px;
    }
    .kiwi-header p {
        color: #94a3b8;
        font-size: 14px;
        margin: 0;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-high { background-color: #fee2e2; color: #ef4444; border: 1px solid #fca5a5; }
    .badge-medium { background-color: #fef3c7; color: #d97706; border: 1px solid #fcd34d; }
    .badge-low { background-color: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; }
    .badge-hot { background-color: #fee2e2; color: #b91c1c; font-weight: bold; }
    .badge-warm { background-color: #ffedd5; color: #c2410c; }
    .badge-cold { background-color: #e0f2fe; color: #0369a1; }
    .step-box {
        padding: 12px 16px;
        background: #f8fafc;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 8px;
    }
    .duplicate-warning {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        padding: 12px 16px;
        border-radius: 8px;
        color: #92400e;
        margin-bottom: 14px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- HELPER FUNCTIONS --------------------

def safe_str(val, fallback="Not specified"):
    if val is None or not str(val).strip():
        return fallback
    return str(val).strip()


def get_lead_tier(score):
    if score >= 80:
        return "🔥 Hot Lead", "badge-hot"
    elif score >= 50:
        return "⚡ Warm Lead", "badge-warm"
    return "❄️ Cold Lead", "badge-cold"


def parse_json_safely(text):
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("### 🥝 Kiwi Connect Digital")
    st.caption("AI Workflow Automation System")

    st.markdown("---")

    page = st.radio(
        "Navigation Menu",
        [
            "📊 Executive Dashboard",
            "📝 Enquiry Intake Form",
            "📋 Lead Management CRM",
            "⚡ Visual Workflow Pipeline",
            "🧪 AI Analysis Lab",
            "📖 Architecture & Interview Guide"
        ]
    )

    st.markdown("---")

    st.markdown("#### ⚙️ Quick System Actions")

    if st.button("🌱 Load Realistic Sample Leads", use_container_width=True):
        import seed_data
        with st.spinner("Seeding database with verified test leads..."):
            seed_data.seed_database(clear_existing=False)
        st.success("Sample leads loaded successfully!")
        st.rerun()

    with st.expander("⚠️ Database Reset", expanded=False):
        st.caption("Permanently delete all customer records and reset ID sequence.")
        if st.button("🗑️ Clear All Enquiries", type="secondary", use_container_width=True):
            deleted_count = database.delete_all_enquiries()
            st.warning(f"Cleared {deleted_count} enquiries from database.")
            st.rerun()

    st.caption(f"**Database:** SQLite (`enquiries.db`)")
    st.caption(f"**AI Engine:** Google Gemini Flash")
    st.caption(f"**REST API:** `/docs` (FastAPI)")


# -------------------- LOAD DATABASE RECORDS --------------------

all_enquiries = database.get_all_enquiries()
analytics = database.get_analytics_summary()


# ==============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==============================================================================

if page == "📊 Executive Dashboard":

    st.markdown(f"""
    <div class="kiwi-header">
        <h1>📊 Executive Lead Intelligence Dashboard</h1>
        <p>{config.COMPANY_NAME} — Automated Enquiry Processing, AI Lead Scoring, and Performance Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # Key Performance Indicators
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    kpi1.metric("Total Enquiries", analytics["total"])
    kpi2.metric("New Leads", analytics["new"], help="Awaiting initial sales outreach")
    kpi3.metric("High Priority", analytics["high_priority"], delta="Requires urgent follow-up")
    kpi4.metric("In Progress", analytics["in_progress"])
    kpi5.metric("Converted", analytics["converted"])
    kpi6.metric("Conversion Rate", f"{analytics['conversion_rate']}%")

    # Lead Score & Conversion Bar
    col_lead_score, col_conversion = st.columns(2)
    with col_lead_score:
        st.markdown(f"**Average Lead Quality Score:** `{analytics['avg_lead_score']} / 100`")
        st.progress(min(1.0, analytics["avg_lead_score"] / 100.0))

    with col_conversion:
        st.markdown(f"**Sales Funnel Conversion Progress:** `{analytics['conversion_rate']}%`")
        st.progress(min(1.0, analytics["conversion_rate"] / 100.0))

    st.markdown("---")

    # Visual Charts
    col_chart_left, col_chart_right = st.columns(2)

    with col_chart_left:
        st.subheader("Category-Wise Enquiry Distribution")
        cat_counts = analytics["category_counts"]
        if cat_counts:
            df_cat = pd.DataFrame({
                "Category": list(cat_counts.keys()),
                "Enquiries": list(cat_counts.values())
            }).set_index("Category")
            st.bar_chart(df_cat, color="#10b981")
        else:
            st.info("No enquiry data available yet.")

    with col_chart_right:
        st.subheader("Lead Priority & Status Funnel")
        pri_counts = analytics["priority_counts"]
        status_counts = analytics["status_counts"]

        df_pri_status = pd.DataFrame({
            "Metric": ["High Pri", "Med Pri", "Low Pri", "New", "In Progress", "Converted"],
            "Count": [
                pri_counts.get("High", 0),
                pri_counts.get("Medium", 0),
                pri_counts.get("Low", 0),
                status_counts.get("New", 0),
                status_counts.get("In Progress", 0),
                status_counts.get("Converted", 0)
            ]
        }).set_index("Metric")
        st.bar_chart(df_pri_status, color="#3b82f6")

    st.markdown("---")

    # Recent Enquiries Feed
    st.subheader("Recent Customer Activity")
    if all_enquiries:
        recent_display = []
        for e in all_enquiries[:8]:
            score = e.get("lead_score", 50)
            tier, _ = get_lead_tier(score)
            recent_display.append({
                "ID": f"#{e['id']}",
                "Customer": e["customer_name"],
                "Category": e.get("category") or "Unclassified",
                "Priority": e.get("priority") or "Medium",
                "Lead Score": f"{score}/100 ({tier})",
                "Status": e.get("status") or "New",
                "Assigned Specialist": e.get("assigned_to") or "Unassigned",
                "Received": e.get("created_at")
            })

        st.dataframe(pd.DataFrame(recent_display), use_container_width=True, hide_index=True)
    else:
        st.info("No enquiries registered yet. Submit your first enquiry or click 'Load Realistic Sample Leads' in the sidebar.")


# ==============================================================================
# PAGE 2: ENQUIRY INTAKE FORM (SUBMISSION SYSTEM)
# ==============================================================================

elif page == "📝 Enquiry Intake Form":

    st.markdown(f"""
    <div class="kiwi-header">
        <h1>📝 Customer Enquiry Intake & Automated AI Pipeline</h1>
        <p>Submit customer requirements manually or load an official demo preset to watch the AI extraction pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    # Demo Presets Bar
    st.markdown("#### ⚡ 1-Click Demo Presets")
    st.caption("Click any preset below to automatically populate the form with realistic test data:")

    preset_cols = st.columns(len(config.SAMPLE_PRESETS))
    for idx, preset in enumerate(config.SAMPLE_PRESETS):
        with preset_cols[idx]:
            if st.button(preset["title"], key=f"preset_btn_{idx}", use_container_width=True):
                st.session_state["form_name"] = preset["name"]
                st.session_state["form_phone"] = preset["phone"]
                st.session_state["form_email"] = preset["email"]
                st.session_state["form_message"] = preset["message"]
                st.rerun()

    st.markdown("---")

    # Form Submission
    with st.form("enquiry_intake_form"):
        st.subheader("Submit Customer Enquiry")

        col_name, col_phone, col_email = st.columns(3)
        with col_name:
            name_val = st.text_input("Customer Name *", value=st.session_state.get("form_name", ""), placeholder="e.g. Rajesh Gupta")
        with col_phone:
            phone_val = st.text_input("Phone Number", value=st.session_state.get("form_phone", ""), placeholder="e.g. +91 98260 12345")
        with col_email:
            email_val = st.text_input("Email Address", value=st.session_state.get("form_email", ""), placeholder="e.g. rajesh@store.in")

        message_val = st.text_area(
            "Enquiry Message *",
            value=st.session_state.get("form_message", ""),
            height=140,
            placeholder="Describe customer's project, requirements, budget, location, and timeline (e.g. 'I own a clothing store in Indore. I need an e-commerce website with online payments. My budget is around ₹50,000.')"
        )

        submitted = st.form_submit_button("🚀 Submit Enquiry & Run Automated AI Pipeline", use_container_width=True)

    if submitted:
        if not name_val.strip() or not message_val.strip():
            st.error("⚠️ Customer Name and Enquiry Message are mandatory.")
        else:
            # Step 1: Duplicate Detection
            is_dup, dup_id, dup_reason = database.check_duplicate(
                customer_name=name_val,
                phone=phone_val,
                email=email_val,
                message=message_val
            )

            # Step 2: Save to Database
            enquiry_id = database.add_enquiry(
                customer_name=name_val,
                phone=phone_val,
                email=email_val,
                message=message_val
            )

            # Step 3: Run AI Workflow with Progress
            progress_bar = st.progress(0.1)
            status_text = st.empty()

            try:
                status_text.text("⚡ Step 1/4: Ingesting customer enquiry into database...")
                progress_bar.progress(0.3)

                status_text.text("🤖 Step 2/4: Gemini AI analyzing message, extracting requirements, and classifying service...")
                analysis = ai_engine.analyze_enquiry(message_val)
                progress_bar.progress(0.7)

                status_text.text("📊 Step 3/4: Scoring lead quality, generating response, and routing to team...")
                database.save_ai_analysis(
                    enquiry_id=enquiry_id,
                    analysis=analysis,
                    is_duplicate=is_dup,
                    duplicate_of_id=dup_id
                )
                progress_bar.progress(1.0)
                status_text.text("✅ Step 4/4: Pipeline executed successfully!")

                # Display Results Card
                st.success(f"🎉 Enquiry #{enquiry_id} processed and saved to database!")

                if is_dup:
                    st.warning(f"⚠️ **Duplicate Detection Alert:** {dup_reason}")

                # Analysis Card
                with st.container(border=True):
                    st.markdown(f"### 📋 AI Extraction Results for Enquiry #{enquiry_id}")

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Category", analysis["category"])
                    c2.metric("Stated Budget", safe_str(analysis.get("budget")))
                    c3.metric("Location", safe_str(analysis.get("location")))
                    c4.metric("Urgency", analysis.get("urgency", "Unknown"))

                    c5, c6, c7, c8 = st.columns(4)
                    tier, _ = get_lead_tier(analysis.get("lead_score", 50))
                    c5.metric("Priority Level", analysis["priority"])
                    c6.metric("Lead Score", f"{analysis.get('lead_score', 50)}/100")
                    c7.metric("Lead Tier", tier)
                    c8.metric("Assigned Specialist", database.TEAM_ROUTING.get(analysis["category"], "Support Lead"))

                    st.markdown(f"**Executive Summary:** {analysis.get('summary')}")
                    st.markdown(f"**Priority Reasoning:** {analysis.get('priority_reason')}")

                    col_req, col_missing = st.columns(2)
                    with col_req:
                        st.markdown("**🎯 Extracted Requirements:**")
                        for req in analysis.get("requirements", []):
                            st.markdown(f"- {req}")

                    with col_missing:
                        st.markdown("**❓ Missing Information Needed:**")
                        for m in analysis.get("missing_information", []):
                            st.markdown(f"- {m}")

                    st.markdown("**💬 AI-Generated Customer Response:**")
                    st.info(analysis["suggested_response"])

                    st.caption(f"Engine: {analysis.get('source')} | Latency: {analysis.get('latency_seconds', 0)}s")

            except Exception as e:
                st.error(f"AI Pipeline execution encountered an issue: {e}")
                st.exception(e)


# ==============================================================================
# PAGE 3: LEAD MANAGEMENT CRM (ALL ENQUIRIES)
# ==============================================================================

elif page == "📋 Lead Management CRM":

    st.markdown(f"""
    <div class="kiwi-header">
        <h1>📋 Lead Management & CRM Hub</h1>
        <p>Search, filter, inspect AI extractions, edit suggested responses, and manage customer communications.</p>
    </div>
    """, unsafe_allow_html=True)

    if not all_enquiries:
        st.info("No enquiries registered in the database. Use the 'Enquiry Intake Form' or 'Load Realistic Sample Leads' to get started.")
        st.stop()

    # Filters Bar
    col_search, col_cat, col_pri, col_stat = st.columns(4)
    with col_search:
        search_query = st.text_input("🔍 Search Leads", placeholder="Search name, email, phone, keyword...")
    with col_cat:
        cat_filter = st.selectbox("Filter Category", ["All"] + config.CATEGORIES + ["Unclassified"])
    with col_pri:
        pri_filter = st.selectbox("Filter Priority", ["All"] + config.PRIORITIES)
    with col_stat:
        stat_filter = st.selectbox("Filter Status", ["All"] + config.STATUSES)

    # Filter enquiries
    filtered = []
    for e in all_enquiries:
        cat = e.get("category") or "Unclassified"
        pri = e.get("priority") or "Medium"
        stat = e.get("status") or "New"

        if cat_filter != "All" and cat != cat_filter:
            continue
        if pri_filter != "All" and pri != pri_filter:
            continue
        if stat_filter != "All" and stat != stat_filter:
            continue

        if search_query.strip():
            haystack = f"{e['customer_name']} {e.get('email', '')} {e.get('phone', '')} {e.get('message', '')} {e.get('summary', '')}".lower()
            if search_query.strip().lower() not in haystack:
                continue

        filtered.append(e)

    st.markdown(f"Displaying **{len(filtered)}** of **{len(all_enquiries)}** total customer leads")

    # Table view
    table_data = []
    for e in filtered:
        score = e.get("lead_score", 50)
        tier, _ = get_lead_tier(score)
        table_data.append({
            "ID": e["id"],
            "Customer": e["customer_name"],
            "Category": e.get("category") or "Unclassified",
            "Priority": e.get("priority") or "Medium",
            "Score": f"{score} ({tier})",
            "Budget": safe_str(e.get("budget"), "—"),
            "Location": safe_str(e.get("location"), "—"),
            "Status": e.get("status") or "New",
            "Assigned To": e.get("assigned_to") or "—",
            "Duplicate": "⚠️ Yes" if e.get("is_duplicate") else "No"
        })

    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Detailed Lead Inspector
    st.subheader("🔍 Detailed Lead Inspector & Action Center")

    lead_ids = [e["id"] for e in filtered]
    if not lead_ids:
        st.warning("No leads match current filter criteria.")
        st.stop()

    selected_id = st.selectbox(
        "Select an Enquiry to Inspect & Manage:",
        lead_ids,
        format_func=lambda x: f"Enquiry #{x} — {next(e['customer_name'] for e in filtered if e['id'] == x)} ({next(e.get('category', 'Unclassified') for e in filtered if e['id'] == x)})"
    )

    lead = next(e for e in filtered if e["id"] == selected_id)

    with st.container(border=True):
        # Duplicate Banner
        if lead.get("is_duplicate"):
            st.markdown(f"""
            <div class="duplicate-warning">
                ⚠️ <strong>Duplicate Lead Alert:</strong> This enquiry has been identified as a duplicate of <strong>Enquiry #{lead.get('duplicate_of_id')}</strong>.
            </div>
            """, unsafe_allow_html=True)

        top_col1, top_col2, top_col3 = st.columns(3)
        with top_col1:
            st.markdown(f"**Customer:** `{lead['customer_name']}`")
            st.markdown(f"**Phone:** `{safe_str(lead.get('phone'))}`")
            st.markdown(f"**Email:** `{safe_str(lead.get('email'))}`")

        with top_col2:
            st.markdown(f"**Category:** `{safe_str(lead.get('category'))}`")
            st.markdown(f"**Budget:** `{safe_str(lead.get('budget'))}`")
            st.markdown(f"**Location:** `{safe_str(lead.get('location'))}`")

        with top_col3:
            score = lead.get("lead_score", 50)
            tier, _ = get_lead_tier(score)
            st.markdown(f"**Priority:** `{safe_str(lead.get('priority'))}`")
            st.markdown(f"**Urgency:** `{safe_str(lead.get('urgency'))}`")
            st.markdown(f"**Lead Quality:** `{score}/100` ({tier})")

        st.markdown("**Original Customer Message:**")
        st.info(lead["message"])

        # Structured AI Breakdown
        parsed_ai = parse_json_safely(lead.get("ai_analysis"))

        if parsed_ai:
            with st.expander("📊 Complete AI Structured Extraction & Requirements", expanded=True):
                sub1, sub2 = st.columns(2)
                with sub1:
                    st.markdown("**🎯 Extracted Requirements:**")
                    for req in parsed_ai.get("requirements", []):
                        st.markdown(f"- {req}")
                with sub2:
                    st.markdown("**❓ Missing Information Needed:**")
                    for m in parsed_ai.get("missing_information", []):
                        st.markdown(f"- {m}")

                st.markdown(f"**Next Steps:** {', '.join(parsed_ai.get('next_steps', []))}")
                st.markdown(f"**Follow-up Recommendation:** `{lead.get('follow_up_action', 'Contact client')}` — **{lead.get('follow_up_date', 'Within 48 hours')}**")

        st.markdown("---")

        # Suggested Customer Response & Editor
        st.subheader("💬 AI Suggested Response & Communication Tools")

        initial_response = lead.get("edited_response") or lead.get("ai_response") or ""
        edited_response_text = st.text_area(
            "Review and edit customer response before reaching out:",
            value=initial_response,
            height=140,
            key=f"edit_resp_{selected_id}"
        )

        col_save_resp, col_wa, col_mail = st.columns(3)

        with col_save_resp:
            if st.button("💾 Save Edited Response", key=f"save_btn_{selected_id}", use_container_width=True):
                database.update_edited_response(selected_id, edited_response_text)
                st.success("Custom response saved successfully!")
                st.rerun()

        with col_wa:
            clean_phone = "".join(filter(str.isdigit, lead.get("phone") or ""))
            encoded_msg = urllib.parse.quote(edited_response_text)
            wa_url = f"https://wa.me/{clean_phone}?text={encoded_msg}" if clean_phone else "#"
            if clean_phone:
                st.link_button("💬 Open WhatsApp Web", wa_url, use_container_width=True)
            else:
                st.button("💬 WhatsApp (No phone)", disabled=True, use_container_width=True)

        with col_mail:
            email_addr = (lead.get("email") or "").strip()
            subject = urllib.parse.quote(f"Regarding your enquiry for {lead.get('category', 'services')} - Kiwi Connect Digital")
            encoded_body = urllib.parse.quote(edited_response_text)
            mailto_url = f"mailto:{email_addr}?subject={subject}&body={encoded_body}" if email_addr else "#"
            if email_addr:
                st.link_button("✉️ Draft Email Client", mailto_url, use_container_width=True)
            else:
                st.button("✉️ Email (No address)", disabled=True, use_container_width=True)

        st.markdown("---")

        # Workflow Actions: Status & Assignment Update
        st.subheader("⚡ Lead Status & Assignment Workflow")
        col_st1, col_st2, col_st3 = st.columns(3)

        with col_st1:
            current_status = lead.get("status") if lead.get("status") in config.STATUSES else "New"
            new_st = st.selectbox(
                "Update Lead Status",
                config.STATUSES,
                index=config.STATUSES.index(current_status),
                key=f"status_sel_{selected_id}"
            )
            if st.button("Update Status", key=f"btn_stat_{selected_id}"):
                database.update_status(selected_id, new_st)
                st.success(f"Status changed to {new_st}")
                st.rerun()

        with col_st2:
            current_assignee = lead.get("assigned_to") or "Rahul Sharma (E-Commerce Specialist)"
            all_assignees = list(set(list(config.TEAM_ROUTING.values()) + [current_assignee]))
            new_assign = st.selectbox(
                "Reassign Team Member",
                all_assignees,
                index=all_assignees.index(current_assignee) if current_assignee in all_assignees else 0,
                key=f"assign_sel_{selected_id}"
            )
            if st.button("Update Assignment", key=f"btn_assign_{selected_id}"):
                database.update_assignment(selected_id, new_assign)
                st.success(f"Reassigned to {new_assign}")
                st.rerun()

        with col_st3:
            st.markdown("**AI Retest & Cleanup**")
            if st.button("🔄 Re-run AI Analysis", key=f"btn_reanalyze_{selected_id}", use_container_width=True):
                with st.spinner("Re-analyzing with Gemini AI..."):
                    new_analysis = ai_engine.analyze_enquiry(lead["message"])
                    database.save_ai_analysis(selected_id, new_analysis)
                st.success("Re-analysis complete!")
                st.rerun()

            if st.button("🗑️ Delete Enquiry", key=f"btn_del_{selected_id}", use_container_width=True):
                database.delete_enquiry(selected_id)
                st.warning(f"Enquiry #{selected_id} deleted.")
                st.rerun()

    # Data Export
    st.markdown("---")
    st.subheader("📥 Export Enquiries")
    col_exp_csv, col_exp_json = st.columns(2)

    with col_exp_csv:
        export_df = pd.DataFrame(all_enquiries)
        st.download_button(
            "📥 Download All Enquiries (CSV)",
            data=export_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="kiwi_connect_enquiries.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_exp_json:
        st.download_button(
            "📥 Download All Enquiries (JSON)",
            data=json.dumps(all_enquiries, indent=2, ensure_ascii=False),
            file_name="kiwi_connect_enquiries.json",
            mime="application/json",
            use_container_width=True
        )


# ==============================================================================
# PAGE 4: VISUAL WORKFLOW PIPELINE
# ==============================================================================

elif page == "⚡ Visual Workflow Pipeline":

    st.markdown(f"""
    <div class="kiwi-header">
        <h1>⚡ End-to-End AI Automation Workflow</h1>
        <p>Interactive visual representation of the 9-step automated pipeline mandated in the assignment specification.</p>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("Step 1: Customer Enquiry Ingestion", "Customer or admin submits enquiry via Web Intake Form or REST API (`/api/enquiries`).", "Customer Name, Phone, Email, Message"),
        ("Step 2: Backend Receipt & Sanitization", "Backend validates payload, prevents prompt injection, and stores initial record.", "SQL Transaction initiated, ID generated"),
        ("Step 3: Duplicate Enquiry Detection", "Algorithms check phone, email, and message token similarity against historical records.", "Flags duplicates and links original enquiry"),
        ("Step 4: AI Analysis & Context Understanding", "Google Gemini Flash analyzes intent, domain context, constraints, and business logic.", "Zero-shot structured prompt with system guards"),
        ("Step 5: Structured Entity Extraction", "Extracts Service Category, Budget, Location, Timeline Urgency, Requirements, and Missing Info.", "Type-safe JSON schema enforcement"),
        ("Step 6: Automatic Categorization & Routing", "Maps requirement to 1 of 7 defined categories and assigns specialist team lead.", "Auto-routes to department lead"),
        ("Step 7: Priority & Lead Scoring", "Scores lead 0-100 based on budget, urgency, and completeness; assigns High/Medium/Low priority.", "Calculates conversion probability"),
        ("Step 8: AI Response & Next Steps Generation", "Generates professional customer response with polite inquiries for missing details.", "Ready for review, WhatsApp, or Email outreach"),
        ("Step 9: Database Persistence & CRM Dashboard", "All extracted metadata, timestamps, and scores committed to SQLite database.", "Instant reflection across Admin Dashboard & REST API")
    ]

    for title, desc, data_flow in steps:
        with st.container(border=True):
            st.markdown(f"#### {title}")
            st.markdown(f"**Action:** {desc}")
            st.caption(f"**Data Flow:** `{data_flow}`")

    st.markdown("---")

    st.subheader("System Architecture Diagram")
    st.code("""
+-----------------------------------------------------------------------------------+
|                            CLIENT & INTAKE INTERFACES                             |
|  - Streamlit Web Dashboard (Port 8501)       - FastAPI REST Endpoints (Port 8000) |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             AUTOMATION & ORCHESTRATION                            |
|  - Input Validation & Defense   - Duplicate Detection Engine   - Workflow Router  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                              AI REASONING CORE (LLM)                              |
|  - Google Gemini 3.5 Flash Lite / 3.1 Flash Lite (Fast Structured JSON Generation) |
|  - Resilient Offline / Fallback Heuristic Rule Engine                             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             STORAGE & CRM MANAGEMENT                              |
|  - SQLite Database (`enquiries.db`) with dynamic schema migration & indexes       |
|  - Lead Scoring (0-100)      - WhatsApp / Mailto Launchers   - CSV / JSON Export  |
+-----------------------------------------------------------------------------------+
    """, language="text")


# ==============================================================================
# PAGE 5: AI ANALYSIS LAB (TESTING BENCH)
# ==============================================================================

elif page == "🧪 AI Analysis Lab":

    st.markdown(f"""
    <div class="kiwi-header">
        <h1>🧪 AI Analysis & Prompt Engineering Lab</h1>
        <p>Interactive testing sandbox to test arbitrary customer messages, inspect raw JSON schema extraction, and benchmark latency.</p>
    </div>
    """, unsafe_allow_html=True)

    test_input = st.text_area(
        "Enter customer enquiry to test:",
        value="I own a clothing store in Indore. I need an e-commerce website where customers can browse products, place orders and make online payments. My budget is around ₹50,000.",
        height=140
    )

    col_btn_test, col_model_choice = st.columns([2, 2])
    with col_model_choice:
        selected_model = st.selectbox("LLM Model", ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"])

    if st.button("⚡ Run Real-Time AI Analysis", type="primary", use_container_width=True):
        if not test_input.strip():
            st.warning("Please enter an enquiry message to test.")
        else:
            with st.spinner("AI Engine executing structured reasoning..."):
                result = ai_engine.analyze_enquiry(test_input.strip(), model_override=selected_model)

            st.success("Analysis Complete!")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Category", result.get("category"))
            c2.metric("Stated Budget", safe_str(result.get("budget")))
            c3.metric("Location", safe_str(result.get("location")))
            c4.metric("Urgency", result.get("urgency"))

            st.markdown(f"**Execution Engine:** `{result.get('source')}` | **Latency:** `{result.get('latency_seconds', 0)}s`")

            st.markdown("#### Raw Structured JSON Output:")
            st.json(result)


# ==============================================================================
# PAGE 6: ARCHITECTURE & INTERVIEW GUIDE
# ==============================================================================

elif page == "📖 Architecture & Interview Guide":

    st.markdown(f"""
    <div class="kiwi-header">
        <h1>📖 Technical Architecture & Final Interview Preparation</h1>
        <p>Comprehensive solutions and rationale for all 8 interview discussion questions specified in the assignment document.</p>
    </div>
    """, unsafe_allow_html=True)

    qa_list = [
        ("1. How does your AI workflow operate?",
         "The workflow follows a 9-step automated pipeline: (1) Ingestion via Streamlit UI or FastAPI REST API, (2) Duplicate detection matching phone, email, and message token overlap, (3) Prompt isolation and sanitization, (4) Google Gemini 3.5 Flash Lite structured reasoning, (5) Strict classification into 1 of the 7 allowed Kiwi Connect Digital categories, (6) Extraction of budget, location, urgency, requirements, and missing info, (7) Multi-factor lead scoring (0-100) and priority assignment, (8) Generation of customized response and next steps, and (9) Atomic persistence into SQLite with live reflection on the CRM dashboard."),

        ("2. How does your AI extract structured information?",
         "We leverage Google GenAI's native structured JSON mode (`response_mime_type: 'application/json'`) backed by an explicit JSON schema in the system prompt. To ensure zero runtime exceptions, the extraction is passed through a validation and sanitization layer that validates category membership against defined constants, enforces type constraints (e.g. integer bounds on lead score 0-100), and provides fallback heuristics if the customer omits details."),

        ("3. How do you handle incorrect AI responses?",
         "We implement a three-layer defense: (1) **Validation & Guardrails**: Schema checking automatically clamps invalid categories to 'Other Services' and invalid priorities to 'Medium'. (2) **Human-in-the-Loop Admin Editing**: Administrators can review and edit suggested responses before dispatching them. (3) **Fallback Engine**: If the LLM produces malformed output or is unreachable, the system automatically falls back to deterministic rule-based NLP extraction, ensuring the workflow never breaks."),

        ("4. How would you handle 1,000 enquiries per day?",
         "1,000 enquiries/day (~0.7 enquiries/minute average, peaking at 10-20/minute) is handled easily by: (1) Replacing SQLite with PostgreSQL / MySQL connection pooling (pgBouncer), (2) Decoupling ingestion from AI processing using an asynchronous message queue (Celery + Redis or AWS SQS), (3) Horizontal scaling of FastAPI backend workers in Docker/Kubernetes, and (4) Rate-limit management using token-bucket throttling and exponential backoff retry policies."),

        ("5. How would you reduce AI API costs?",
         "(1) **Prompt Optimization**: Keep system instructions concise and use minimal token representation. (2) **Cost-Effective Models**: Using `gemini-3.5-flash-lite` provides sub-second latency and costs less than 1/10th of frontier models. (3) **Semantic Caching**: Cache common enquiry analyses (e.g., in Redis) so duplicate or near-identical enquiries don't invoke the LLM twice. (4) **Tiered Processing**: Run fast regex/heuristic pre-filters first; only call the LLM when requirements are sufficiently complex."),

        ("6. How would you integrate this system with WhatsApp or a CRM?",
         "For WhatsApp: Utilize the **WhatsApp Business Cloud API** (or Twilio/Meta Graph API) via webhooks. When an enquiry is approved by the admin, an event triggers an outbound WhatsApp template message, and incoming replies are received via webhook. For CRMs: Expose webhooks and REST endpoints to bi-directionally sync leads to HubSpot, Zoho CRM, or Salesforce with lead score and tags."),

        ("7. Which part of your project did you find most challenging?",
         "Balancing high-precision extraction against real-world ambiguous customer input (e.g. informal Indian English, unstated budgets, or colloquial terms like 'Rs 50k' vs '50,000 INR') while guaranteeing 100% schema stability and zero runtime crashes, even in offline environments."),

        ("8. What improvements would you make if given another two days?",
         "(1) Add full OAuth2 / JWT authentication with role-based access control (Admin vs Sales Rep). (2) Connect live WhatsApp Business webhooks for two-way automated conversational intake. (3) Implement vector embeddings (ChromaDB/Pinecone) for semantic duplicate search and RAG-based pricing estimations. (4) Add automated email sending via SendGrid/SMTP.")
    ]

    for question, answer in qa_list:
        with st.expander(f"📌 {question}", expanded=False):
            st.markdown(answer)

    st.markdown("---")

    st.subheader("Database Schema Specification")
    st.markdown("""
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Unique enquiry identifier |
| `customer_name` | TEXT NOT NULL | Customer's full name |
| `phone` | TEXT | Customer contact number |
| `email` | TEXT | Customer email address |
| `message` | TEXT NOT NULL | Original enquiry message |
| `category` | TEXT | 1 of 7 allowed service categories |
| `priority` | TEXT | High, Medium, or Low |
| `urgency` | TEXT | High, Medium, Low, or Unknown |
| `budget` | TEXT | Extracted budget amount |
| `location` | TEXT | Extracted city/region |
| `lead_score` | INTEGER | 0-100 sales qualification score |
| `lead_score_reason` | TEXT | Justification for lead score |
| `summary` | TEXT | Crisp executive summary |
| `assigned_to` | TEXT | Assigned specialist team lead |
| `is_duplicate` | INTEGER | 1 if detected as duplicate, else 0 |
| `duplicate_of_id` | INTEGER | Matched original enquiry ID |
| `follow_up_date` | TEXT | Recommended follow-up timeline |
| `follow_up_action` | TEXT | Recommended next sales action |
| `tags` | TEXT | JSON list of extracted deliverables |
| `ai_analysis` | TEXT | Full raw JSON analysis from LLM |
| `ai_response` | TEXT | Suggested professional customer response |
| `edited_response` | TEXT | Administrator reviewed & edited response |
| `created_at` | TEXT | Timestamp of submission |
| `updated_at` | TEXT | Timestamp of last modification |
    """)
