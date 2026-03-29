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
    "Release Center",
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
open_tickets = sum(1 for ticket in tickets if (ticket.status or "").lower() in {
                   "open", "in progress", "waiting on user"})
critical_tickets = sum(1 for ticket in tickets if (
    ticket.priority or "").lower() == "critical")

success_rate = 0.0
if total_jobs:
    success_rate = round(((total_jobs - failed_jobs) / total_jobs) * 100, 1)

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Jobs Running", running_jobs, "Live execution", "positive")
with col2:
    metric_card("Job Success Rate",
                f"{success_rate}%", "Last observed", "neutral")
with col3:
    metric_card("Open Tickets", open_tickets, "Needs triage",
                "negative" if open_tickets > 6 else "neutral")
with col4:
    metric_card("Critical Tickets", critical_tickets, "Immediate attention",
                "negative" if critical_tickets > 0 else "positive")

left, right = st.columns([1.2, 1])

with left:
    st.markdown("### Quick Launch")
    st.page_link("pages/1_📊_Job_Monitoring.py",
                 label="Open Job Monitoring Dashboard", icon="📊")
    st.page_link("pages/2_🎟️_Smart_Ticketing.py",
                 label="Open Smart Ticketing", icon="🎟️")
    st.page_link("pages/3_🧠_Knowledge_Assistant.py",
                 label="Open Knowledge Assistant", icon="🧠")

    st.markdown("### Platform Highlights")
    st.markdown(
        """
        - AI-assisted ticket triage and summaries
        - SLA visibility for jobs and incidents
        - End-to-end operational context in one place
        - Responsive multi-page UX for desktop and mobile
        """
    )

with right:
    st.markdown("### System Snapshot")
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    st.info(f"Last refreshed: {now}")

    status_rows = [
        {
            "Module": "Job Processing",
            "Health": status_chip("Running" if running_jobs > 0 else "Paused"),
            "Detail": f"{running_jobs} active workloads",
        },
        {
            "Module": "Incident Workflow",
            "Health": status_chip("In Progress" if open_tickets else "Resolved"),
            "Detail": f"{open_tickets} open workflows",
        },
        {
            "Module": "Knowledge Assistant",
            "Health": status_chip("Running"),
            "Detail": "Gemini-enabled expert support",
        },
    ]

    status_df = pd.DataFrame(status_rows)
    st.markdown(status_df.to_html(escape=False, index=False),
                unsafe_allow_html=True)

st.markdown("### Recent Activity")

activity_col1, activity_col2 = st.columns(2)

with activity_col1:
    st.markdown("#### Latest Jobs")
    latest_jobs = sorted(
        jobs, key=lambda item: item.created_at or datetime.min, reverse=True)[:6]
    if latest_jobs:
        jobs_df = pd.DataFrame(
            [
                {
                    "Job ID": item.job_id,
                    "Type": item.job_type,
                    "Status": item.status,
                    "Priority": item.priority,
                    "Duration": f"{item.duration_min} min",
                }
                for item in latest_jobs
            ]
        )
        st.dataframe(jobs_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No job data available yet.")

with activity_col2:
    st.markdown("#### Latest Tickets")
    latest_tickets = sorted(
        tickets, key=lambda item: item.created_at or datetime.min, reverse=True)[:6]
    if latest_tickets:
        tickets_df = pd.DataFrame(
            [
                {
                    "Ticket": item.ticket_no or f"T-{item.id}",
                    "Title": item.title,
                    "Priority": item.priority,
                    "Status": item.status,
                    "Assignee": item.assignee or "Unassigned",
                }
                for item in latest_tickets
            ]
        )
        st.dataframe(tickets_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No ticket data available yet.")
