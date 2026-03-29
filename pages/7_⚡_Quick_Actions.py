from datetime import datetime

import pandas as pd
import streamlit as st

from db import Job, Ticket, get_session, init_db
from ui import inject_global_styles, render_header, status_chip

st.set_page_config(
    page_title="Quick Actions",
    page_icon="⚡",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "Quick Actions",
    "One-click operations for common tasks. Speed up your workflow with instant actions.",
    "Power Tools",
)

session = get_session()
try:
    jobs = session.query(Job).order_by(Job.created_at.desc()).all()
    tickets = session.query(Ticket).order_by(Ticket.created_at.desc()).all()

    running_jobs = [j for j in jobs if j.status == "Running"]
    failed_jobs = [j for j in jobs if j.status == "Failed"]
    queued_jobs = [j for j in jobs if j.status == "Queued"]
    open_tickets = [t for t in tickets if t.status in ["Open", "In Progress"]]
    critical_tickets = [t for t in tickets if t.priority == "Critical"]
    unassigned_tickets = [
        t for t in tickets if not t.assignee or t.assignee == "Unassigned"]
finally:
    session.close()

st.markdown("### 🚀 Job Operations")

job_col1, job_col2, job_col3 = st.columns(3)

with job_col1:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">⏸️ Pause All Running Jobs</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Immediately pause all currently running jobs for maintenance or emergency.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"Pause {len(running_jobs)} Running Jobs", use_container_width=True, disabled=len(running_jobs) == 0):
        session = get_session()
        try:
            for job in session.query(Job).filter(Job.status == "Running").all():
                job.status = "Paused"
                job.last_heartbeat = datetime.utcnow()
            session.commit()
            st.success(f"Paused {len(running_jobs)} jobs successfully!")
            st.rerun()
        finally:
            session.close()

with job_col2:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">▶️ Resume Paused Jobs</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Resume all paused jobs to continue execution.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    paused_jobs = [j for j in jobs if j.status == "Paused"]
    if st.button(f"Resume {len(paused_jobs)} Paused Jobs", use_container_width=True, disabled=len(paused_jobs) == 0):
        session = get_session()
        try:
            now = datetime.utcnow()
            for job in session.query(Job).filter(Job.status == "Paused").all():
                job.status = "Running"
                job.last_heartbeat = now
                if not job.started_at:
                    job.started_at = now
            session.commit()
            st.success(f"Resumed {len(paused_jobs)} jobs!")
            st.rerun()
        finally:
            session.close()

with job_col3:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">🔄 Retry Failed Jobs</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Reset failed jobs to queued status for retry.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"Retry {len(failed_jobs)} Failed Jobs", use_container_width=True, disabled=len(failed_jobs) == 0):
        session = get_session()
        try:
            for job in session.query(Job).filter(Job.status == "Failed").all():
                job.status = "Queued"
                job.started_at = None
                job.ended_at = None
                job.duration_min = 0
                job.last_heartbeat = datetime.utcnow()
            session.commit()
            st.success(f"Queued {len(failed_jobs)} jobs for retry!")
            st.rerun()
        finally:
            session.close()

job_col4, job_col5, job_col6 = st.columns(3)

with job_col4:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">🚀 Start Queued Jobs</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Begin execution of all queued jobs immediately.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"Start {len(queued_jobs)} Queued Jobs", use_container_width=True, disabled=len(queued_jobs) == 0):
        session = get_session()
        try:
            now = datetime.utcnow()
            for job in session.query(Job).filter(Job.status == "Queued").all():
                job.status = "Running"
                job.started_at = now
                job.last_heartbeat = now
            session.commit()
            st.success(f"Started {len(queued_jobs)} jobs!")
            st.rerun()
        finally:
            session.close()

with job_col5:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">⏱️ Advance Time +5 Min</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Simulate time progression for running jobs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Simulate +5 Minutes", use_container_width=True, disabled=len(running_jobs) == 0):
        session = get_session()
        try:
            now = datetime.utcnow()
            count = 0
            for job in session.query(Job).filter(Job.status == "Running").all():
                job.duration_min = (job.duration_min or 0) + 5
                job.last_heartbeat = now
                count += 1
            session.commit()
            st.success(f"Advanced {count} jobs by 5 minutes!")
            st.rerun()
        finally:
            session.close()

with job_col6:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">✅ Complete All Running</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Mark all running jobs as completed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Complete All Running", use_container_width=True, disabled=len(running_jobs) == 0):
        session = get_session()
        try:
            now = datetime.utcnow()
            for job in session.query(Job).filter(Job.status == "Running").all():
                job.status = "Completed"
                job.ended_at = now
                job.last_heartbeat = now
            session.commit()
            st.success(f"Completed {len(running_jobs)} jobs!")
            st.rerun()
        finally:
            session.close()

st.markdown("---")
st.markdown("### 🎟️ Ticket Operations")

ticket_col1, ticket_col2, ticket_col3 = st.columns(3)

with ticket_col1:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">👤 Assign Unassigned</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Assign all unassigned tickets to a team member.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    assignee_name = st.text_input(
        "Assignee Name", placeholder="Enter assignee name", key="bulk_assignee")
    if st.button(f"Assign {len(unassigned_tickets)} Tickets", use_container_width=True, disabled=len(unassigned_tickets) == 0 or not assignee_name.strip()):
        session = get_session()
        try:
            now = datetime.utcnow()
            for ticket in session.query(Ticket).filter((Ticket.assignee.is_(None)) | (Ticket.assignee == "Unassigned")).all():
                ticket.assignee = assignee_name.strip()
                ticket.updated_at = now
            session.commit()
            st.success(
                f"Assigned {len(unassigned_tickets)} tickets to {assignee_name}!")
            st.rerun()
        finally:
            session.close()

with ticket_col2:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">🔥 Escalate Critical</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Move all critical tickets to "In Progress" status.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    open_critical = [t for t in critical_tickets if t.status == "Open"]
    if st.button(f"Escalate {len(open_critical)} Critical", use_container_width=True, disabled=len(open_critical) == 0):
        session = get_session()
        try:
            now = datetime.utcnow()
            for ticket in session.query(Ticket).filter(Ticket.priority == "Critical", Ticket.status == "Open").all():
                ticket.status = "In Progress"
                ticket.updated_at = now
            session.commit()
            st.success(f"Escalated {len(open_critical)} critical tickets!")
            st.rerun()
        finally:
            session.close()

with ticket_col3:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">✅ Resolve Low Priority</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Auto-resolve all low priority tickets.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    low_tickets = [t for t in tickets if t.priority ==
                   "Low" and t.status in ["Open", "In Progress"]]
    if st.button(f"Resolve {len(low_tickets)} Low Priority", use_container_width=True, disabled=len(low_tickets) == 0):
        session = get_session()
        try:
            now = datetime.utcnow()
            for ticket in session.query(Ticket).filter(Ticket.priority == "Low", Ticket.status.in_(["Open", "In Progress"])).all():
                ticket.status = "Resolved"
                ticket.resolution = "Auto-resolved via bulk action"
                ticket.updated_at = now
            session.commit()
            st.success(f"Resolved {len(low_tickets)} low priority tickets!")
            st.rerun()
        finally:
            session.close()

st.markdown("---")
st.markdown("### 📊 Current Status Overview")

overview_col1, overview_col2 = st.columns(2)

with overview_col1:
    st.markdown("#### Jobs by Status")
    job_status_counts = {}
    for job in jobs:
        status = job.status or "Unknown"
        job_status_counts[status] = job_status_counts.get(status, 0) + 1

    for status, count in sorted(job_status_counts.items()):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span>{status_chip(status)}</span>
                <span style="font-weight: 600; color: var(--text-primary);">{count}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

with overview_col2:
    st.markdown("#### Tickets by Status")
    ticket_status_counts = {}
    for ticket in tickets:
        status = ticket.status or "Unknown"
        ticket_status_counts[status] = ticket_status_counts.get(status, 0) + 1

    for status, count in sorted(ticket_status_counts.items()):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span>{status_chip(status)}</span>
                <span style="font-weight: 600; color: var(--text-primary);">{count}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown("### ⚠️ Danger Zone")

danger_col1, danger_col2 = st.columns(2)

with danger_col1:
    st.markdown(
        """
        <div class="surface-card" style="border-left: 3px solid #f43f5e;">
            <div style="font-weight: 600; color: #f43f5e; margin-bottom: 0.5rem;">🗑️ Clear Completed Jobs</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Permanently remove all completed jobs from the database.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    completed_jobs = [j for j in jobs if j.status == "Completed"]
    confirm_delete_jobs = st.checkbox(
        "I understand this action cannot be undone", key="confirm_jobs")
    if st.button(f"Delete {len(completed_jobs)} Completed Jobs", use_container_width=True, disabled=len(completed_jobs) == 0 or not confirm_delete_jobs, type="primary"):
        session = get_session()
        try:
            session.query(Job).filter(Job.status == "Completed").delete()
            session.commit()
            st.success(f"Deleted {len(completed_jobs)} completed jobs!")
            st.rerun()
        finally:
            session.close()

with danger_col2:
    st.markdown(
        """
        <div class="surface-card" style="border-left: 3px solid #f43f5e;">
            <div style="font-weight: 600; color: #f43f5e; margin-bottom: 0.5rem;">🗑️ Clear Closed Tickets</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                Permanently remove all closed tickets from the database.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    closed_tickets = [t for t in tickets if t.status == "Closed"]
    confirm_delete_tickets = st.checkbox(
        "I understand this action cannot be undone", key="confirm_tickets")
    if st.button(f"Delete {len(closed_tickets)} Closed Tickets", use_container_width=True, disabled=len(closed_tickets) == 0 or not confirm_delete_tickets, type="primary"):
        session = get_session()
        try:
            session.query(Ticket).filter(Ticket.status == "Closed").delete()
            session.commit()
            st.success(f"Deleted {len(closed_tickets)} closed tickets!")
            st.rerun()
        finally:
            session.close()
