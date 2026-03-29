from datetime import datetime

import pandas as pd
import streamlit as st

from db import Job, Ticket, get_session, init_db
from ui import inject_global_styles, metric_card, render_header, status_chip

st.set_page_config(
    page_title="Enterprise Ops Hub",
    page_icon="🚀",
    layout="wide",
)

inject_global_styles()
init_db()

render_header(
    "Enterprise Ops Hub",
    "Monitor pipelines, resolve incidents, and collaborate with AI in one streamlined workspace.",
    "Command Center",
)

session = get_session()
try:
    jobs = session.query(Job).all()
    tickets = session.query(Ticket).all()
finally:
    session.close()

total_jobs = len(jobs)
running_jobs = sum(1 for job in jobs if (
    job.status or "").lower() == "running")
failed_jobs = sum(1 for job in jobs if (job.status or "").lower() == "failed")
queued_jobs = sum(1 for job in jobs if (job.status or "").lower() == "queued")
open_tickets = sum(1 for ticket in tickets if (ticket.status or "").lower() in {
                   "open", "in progress", "waiting on user"})
critical_tickets = sum(1 for ticket in tickets if (
    ticket.priority or "").lower() == "critical")

sla_breaches = sum(1 for job in jobs if (job.duration_min or 0) > (job.sla_min or 0)
                   and (job.status or "").lower() in {"running", "completed", "failed"})

success_rate = 0.0
if total_jobs:
    success_rate = round(((total_jobs - failed_jobs) / total_jobs) * 100, 1)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    metric_card("Running Jobs", running_jobs, "Active now",
                "positive" if running_jobs > 0 else "neutral")
with col2:
    metric_card("Queued", queued_jobs, "Waiting", "neutral")
with col3:
    metric_card("Success Rate", f"{success_rate}%", "Overall", "positive" if success_rate >=
                90 else "negative" if success_rate < 70 else "neutral")
with col4:
    metric_card("Open Tickets", open_tickets, "Needs attention",
                "negative" if open_tickets > 6 else "neutral")
with col5:
    metric_card("Critical", critical_tickets, "Urgent",
                "negative" if critical_tickets > 0 else "positive")
with col6:
    metric_card("SLA Breaches", sla_breaches, "At risk",
                "negative" if sla_breaches > 0 else "positive")

st.markdown("---")

left, right = st.columns([1.4, 1])

with left:
    st.markdown("### 🚀 Quick Launch")

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        st.page_link("pages/1_📊_Job_Monitoring.py",
                     label="📊 Job Monitoring", icon="📊")
        st.page_link("pages/2_🎟️_Smart_Ticketing.py",
                     label="🎟️ Smart Ticketing", icon="🎟️")
        st.page_link("pages/3_🧠_Knowledge_Assistant.py",
                     label="🧠 Knowledge Assistant", icon="🧠")
        st.page_link("pages/4_💓_System_Health.py",
                     label="💓 System Health", icon="💓")

    with nav_col2:
        st.page_link("pages/5_📜_Audit_Log.py", label="📜 Audit Log", icon="📜")
        st.page_link("pages/6_⏱️_SLA_Dashboard.py",
                     label="⏱️ SLA Dashboard", icon="⏱️")
        st.page_link("pages/7_⚡_Quick_Actions.py",
                     label="⚡ Quick Actions", icon="⚡")
        st.page_link("pages/8_🔍_Global_Search.py",
                     label="🔍 Global Search", icon="🔍")

    st.markdown("### ✨ Platform Features")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.markdown(
            """
            <div class="surface-card" style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">🤖 AI-Powered Triage</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">Automatic ticket categorization with Google Gemini</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="surface-card" style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">⏱️ SLA Intelligence</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">Real-time SLA tracking with breach alerts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with feature_col2:
        st.markdown(
            """
            <div class="surface-card" style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">📊 Live Monitoring</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">Real-time job status and system health</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="surface-card" style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">🔍 Universal Search</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">Search across all jobs, tickets, and activities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right:
    st.markdown("### 🌡️ System Status")

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    st.caption(f"Last updated: {now}")

    overall_status = "Healthy"
    if failed_jobs > 2 or critical_tickets > 0:
        overall_status = "Critical"
    elif failed_jobs > 0 or sla_breaches > 0:
        overall_status = "Degraded"

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: var(--text-muted);">Overall:</div>
            {status_chip(overall_status)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    modules = [
        {"name": "Job Scheduler", "status": "Running" if running_jobs >
            0 or queued_jobs > 0 else "Idle", "detail": f"{running_jobs} active"},
        {"name": "Ticket System", "status": "Active" if open_tickets >
            0 else "Idle", "detail": f"{open_tickets} open"},
        {"name": "AI Assistant", "status": "Running", "detail": "Gemini ready"},
        {"name": "SLA Monitor", "status": "Alert" if sla_breaches >
            0 else "Running", "detail": f"{sla_breaches} breaches"},
    ]

    for module in modules:
        status_color = "#10b981" if module["status"] in [
            "Running", "Active", "Idle"] else "#f59e0b" if module["status"] == "Alert" else "#f43f5e"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color}; box-shadow: 0 0 8px {status_color};"></div>
                    <span style="color: var(--text-primary); font-weight: 500;">{module['name']}</span>
                </div>
                <span style="color: var(--text-muted); font-size: 0.85rem;">{module['detail']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown("### 📈 Recent Activity")

activity_col1, activity_col2 = st.columns(2)

with activity_col1:
    st.markdown("#### Latest Jobs")
    latest_jobs = sorted(
        jobs, key=lambda item: item.created_at or datetime.min, reverse=True)[:6]
    if latest_jobs:
        for job in latest_jobs:
            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 0.5rem; padding: 0.75rem 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-weight: 600; color: var(--accent-cyan);">{job.job_id}</span>
                            <span style="color: var(--text-muted); font-size: 0.85rem;">{job.job_type}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            {status_chip(job.status)}
                            {status_chip(job.priority)}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("No job data available yet.")

with activity_col2:
    st.markdown("#### Latest Tickets")
    latest_tickets = sorted(
        tickets, key=lambda item: item.created_at or datetime.min, reverse=True)[:6]
    if latest_tickets:
        for ticket in latest_tickets:
            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 0.5rem; padding: 0.75rem 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-weight: 600; color: var(--accent-violet);">{ticket.ticket_no or f'T-{ticket.id}'}</span>
                            <span style="color: var(--text-secondary); font-size: 0.85rem; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{ticket.title}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            {status_chip(ticket.status)}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("No ticket data available yet.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 1rem; color: var(--text-muted); font-size: 0.85rem;">
        <div>Enterprise Ops Hub v2.0 • Powered by Streamlit & Google Gemini</div>
        <div style="margin-top: 0.25rem;">Made with 💜 for modern operations teams</div>
    </div>
    """,
    unsafe_allow_html=True,
)
