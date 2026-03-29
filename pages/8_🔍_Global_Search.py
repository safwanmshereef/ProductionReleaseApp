from datetime import datetime

import pandas as pd
import streamlit as st

from db import Job, Ticket, TicketActivity, get_session, init_db
from ui import inject_global_styles, render_header, status_chip

st.set_page_config(
    page_title="Global Search",
    page_icon="🔍",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "Global Search",
    "Search across jobs, tickets, and activities instantly. Find anything in seconds.",
    "Universal Search",
)

search_query = st.text_input(
    "🔍 Search anything...",
    placeholder="Enter job ID, ticket title, description, assignee, notes...",
    key="global_search",
)

search_col1, search_col2, search_col3 = st.columns([1, 1, 2])
with search_col1:
    search_scope = st.multiselect(
        "Search in",
        ["Jobs", "Tickets", "Activities"],
        default=["Jobs", "Tickets", "Activities"],
    )
with search_col2:
    result_limit = st.selectbox("Max results per category", [
                                10, 25, 50, 100], index=0)

if search_query.strip():
    needle = search_query.lower().strip()

    session = get_session()
    try:
        job_results = []
        ticket_results = []
        activity_results = []

        if "Jobs" in search_scope:
            jobs = session.query(Job).all()
            for job in jobs:
                searchable = " ".join([
                    str(job.job_id or ""),
                    str(job.job_type or ""),
                    str(job.owner or ""),
                    str(job.status or ""),
                    str(job.priority or ""),
                    str(job.notes or ""),
                ]).lower()

                if needle in searchable:
                    job_results.append(job)
                    if len(job_results) >= result_limit:
                        break

        if "Tickets" in search_scope:
            tickets = session.query(Ticket).all()
            for ticket in tickets:
                searchable = " ".join([
                    str(ticket.ticket_no or ""),
                    str(ticket.title or ""),
                    str(ticket.description or ""),
                    str(ticket.category or ""),
                    str(ticket.status or ""),
                    str(ticket.priority or ""),
                    str(ticket.assignee or ""),
                    str(ticket.requester or ""),
                    str(ticket.ai_summary or ""),
                    str(ticket.root_cause or ""),
                    str(ticket.resolution or ""),
                ]).lower()

                if needle in searchable:
                    ticket_results.append(ticket)
                    if len(ticket_results) >= result_limit:
                        break

        if "Activities" in search_scope:
            activities = session.query(TicketActivity).order_by(
                TicketActivity.created_at.desc()).all()
            for activity in activities:
                searchable = " ".join([
                    str(activity.actor or ""),
                    str(activity.action or ""),
                    str(activity.note or ""),
                ]).lower()

                if needle in searchable:
                    activity_results.append(activity)
                    if len(activity_results) >= result_limit:
                        break
    finally:
        session.close()

    total_results = len(job_results) + \
        len(ticket_results) + len(activity_results)

    st.markdown(
        f"""
        <div style="padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
            <span style="color: var(--text-primary); font-weight: 600;">
                Found {total_results} results for "{search_query}"
            </span>
            <span style="color: var(--text-muted); margin-left: 1rem;">
                ({len(job_results)} jobs, {len(ticket_results)} tickets, {len(activity_results)} activities)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if job_results:
        st.markdown("### 📊 Jobs")

        for job in job_results:
            highlight_parts = []
            if needle in (job.job_id or "").lower():
                highlight_parts.append("ID")
            if needle in (job.job_type or "").lower():
                highlight_parts.append("Type")
            if needle in (job.notes or "").lower():
                highlight_parts.append("Notes")

            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem;">
                                <span style="font-weight: 700; color: var(--accent-cyan); font-size: 1.1rem;">{job.job_id}</span>
                                <span style="color: var(--text-secondary);">{job.job_type}</span>
                                {status_chip(job.status)}
                                {status_chip(job.priority)}
                            </div>
                            <div style="color: var(--text-muted); font-size: 0.85rem;">
                                Owner: {job.owner or 'Unassigned'} • Duration: {job.duration_min} min • SLA: {job.sla_min} min
                            </div>
                            {f"<div style='color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 6px;'>{job.notes[:200]}{'...' if len(job.notes or '') > 200 else ''}</div>" if job.notes else ""}
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; color: var(--text-muted);">Match in: {', '.join(highlight_parts) if highlight_parts else 'Content'}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if ticket_results:
        st.markdown("### 🎟️ Tickets")

        for ticket in ticket_results:
            highlight_parts = []
            if needle in (ticket.ticket_no or "").lower():
                highlight_parts.append("ID")
            if needle in (ticket.title or "").lower():
                highlight_parts.append("Title")
            if needle in (ticket.description or "").lower():
                highlight_parts.append("Description")
            if needle in (ticket.assignee or "").lower():
                highlight_parts.append("Assignee")

            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem;">
                                <span style="font-weight: 700; color: var(--accent-violet); font-size: 1.1rem;">{ticket.ticket_no}</span>
                                {status_chip(ticket.status)}
                                {status_chip(ticket.priority)}
                                <span style="color: var(--text-muted); font-size: 0.8rem;">{ticket.category}</span>
                            </div>
                            <div style="color: var(--text-primary); font-weight: 500; margin-bottom: 0.25rem;">{ticket.title}</div>
                            <div style="color: var(--text-muted); font-size: 0.85rem;">
                                Assignee: {ticket.assignee or 'Unassigned'} • Requester: {ticket.requester or 'Unknown'}
                            </div>
                            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 6px;">
                                {ticket.description[:250]}{'...' if len(ticket.description or '') > 250 else ''}
                            </div>
                        </div>
                        <div style="text-align: right; margin-left: 1rem;">
                            <div style="font-size: 0.75rem; color: var(--text-muted);">Match in: {', '.join(highlight_parts) if highlight_parts else 'Content'}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if activity_results:
        st.markdown("### 📜 Activities")

        for activity in activity_results:
            session = get_session()
            try:
                ticket = session.query(Ticket).filter(
                    Ticket.id == activity.ticket_id).first()
                ticket_ref = ticket.ticket_no if ticket else f"Ticket #{activity.ticket_id}"
            finally:
                session.close()

            created_str = activity.created_at.strftime(
                "%Y-%m-%d %H:%M") if activity.created_at else "Unknown"

            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem;">
                                <span style="color: var(--accent-cyan);">{ticket_ref}</span>
                                <span style="padding: 0.2rem 0.5rem; border-radius: 4px; background: rgba(139,92,246,0.15); color: #a78bfa; font-size: 0.75rem; font-weight: 600;">{activity.action}</span>
                            </div>
                            <div style="color: var(--text-secondary); font-size: 0.9rem;">{activity.note or 'No details'}</div>
                            <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 0.25rem;">
                                by {activity.actor or 'System'} • {created_str}
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if total_results == 0:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <div style="font-size: 1.1rem;">No results found</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Try a different search term or expand your search scope</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

else:
    st.markdown(
        """
        <div style="text-align: center; padding: 4rem 2rem; color: var(--text-muted);">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🔍</div>
            <div style="font-size: 1.25rem; color: var(--text-primary); margin-bottom: 0.75rem;">Search Across Everything</div>
            <div style="font-size: 0.95rem; max-width: 500px; margin: 0 auto; line-height: 1.6;">
                Enter a search term above to find jobs, tickets, and activities. 
                Search by ID, title, description, assignee, owner, notes, and more.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Search Tips")

    tips_col1, tips_col2, tips_col3 = st.columns(3)

    with tips_col1:
        st.markdown(
            """
            <div class="surface-card">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">🔢 Search by ID</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">
                    Enter <code style="background: rgba(255,255,255,0.05); padding: 0.1rem 0.3rem; border-radius: 4px;">JOB-1001</code> or 
                    <code style="background: rgba(255,255,255,0.05); padding: 0.1rem 0.3rem; border-radius: 4px;">TKT-1002</code> to find specific items.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tips_col2:
        st.markdown(
            """
            <div class="surface-card">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">👤 Search by Person</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">
                    Enter a name like <code style="background: rgba(255,255,255,0.05); padding: 0.1rem 0.3rem; border-radius: 4px;">Ravi</code> to find 
                    all items assigned to or created by that person.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tips_col3:
        st.markdown(
            """
            <div class="surface-card">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">📝 Search Content</div>
                <div style="color: var(--text-secondary); font-size: 0.85rem;">
                    Enter keywords like <code style="background: rgba(255,255,255,0.05); padding: 0.1rem 0.3rem; border-radius: 4px;">ETL</code> or 
                    <code style="background: rgba(255,255,255,0.05); padding: 0.1rem 0.3rem; border-radius: 4px;">failed</code> to search descriptions and notes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 📊 Quick Stats")

    session = get_session()
    try:
        total_jobs = session.query(Job).count()
        total_tickets = session.query(Ticket).count()
        total_activities = session.query(TicketActivity).count()
    finally:
        session.close()

    stats_col1, stats_col2, stats_col3 = st.columns(3)

    with stats_col1:
        st.metric("Total Jobs", total_jobs)
    with stats_col2:
        st.metric("Total Tickets", total_tickets)
    with stats_col3:
        st.metric("Total Activities", total_activities)
