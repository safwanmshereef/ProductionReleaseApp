from datetime import datetime
from typing import Any, cast

import pandas as pd
import plotly.express as px
import streamlit as st

from ai_service import triage_ticket
from db import (
    TICKET_STATUS_OPTIONS,
    Ticket,
    TicketActivity,
    add_ticket_activity,
    get_session,
    init_db,
    next_ticket_number,
)
from ui import inject_global_styles, metric_card, render_header, status_chip

st.set_page_config(page_title="Smart Ticketing", page_icon="🎟️", layout="wide")

inject_global_styles()
init_db()
render_header(
    "Smart Ticketing",
    "Triage faster, assign ownership, and drive incidents to resolution with confidence.",
    "Incident Command",
)


def _fetch_all_data():
    session = get_session()
    try:
        tickets = session.query(Ticket).order_by(
            Ticket.created_at.desc()).all()
        activities = session.query(TicketActivity).order_by(
            TicketActivity.created_at.desc()).all()
        return tickets, activities
    finally:
        session.close()


tickets, activities = _fetch_all_data()

tickets_df = pd.DataFrame(
    [
        {
            "ID": ticket.id,
            "Ticket": ticket.ticket_no or f"T-{ticket.id}",
            "Title": ticket.title,
            "Priority": ticket.priority,
            "Category": ticket.category,
            "Status": ticket.status,
            "Impact": ticket.impact or "Medium",
            "Requester": ticket.requester or "Unknown",
            "Assignee": ticket.assignee or "Unassigned",
            "Created": ticket.created_at,
            "Updated": ticket.updated_at,
        }
        for ticket in tickets
    ]
)

if not tickets_df.empty:
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([
                                                                    1.5, 1, 1, 0.3])
    with filter_col1:
        search_text = st.text_input(
            "Search ticket", placeholder="Title, ID, assignee")
    with filter_col2:
        status_filter = st.multiselect(
            "Status", TICKET_STATUS_OPTIONS, default=TICKET_STATUS_OPTIONS)
    with filter_col3:
        priority_filter = st.multiselect(
            "Priority", ["Low", "Medium", "High", "Critical"], default=["Low", "Medium", "High", "Critical"]
        )
    with filter_col4:
        st.markdown("<div style='height: 28px;'></div>",
                    unsafe_allow_html=True)
        if st.button("🔄", help="Refresh data", use_container_width=True, key="refresh_tickets"):
            st.rerun()

    filtered_tickets_df = tickets_df.copy()
    if search_text:
        needle = search_text.lower().strip()
        filtered_tickets_df = filtered_tickets_df[
            filtered_tickets_df["Ticket"].str.lower().str.contains(needle)
            | filtered_tickets_df["Title"].str.lower().str.contains(needle)
            | filtered_tickets_df["Assignee"].str.lower().str.contains(needle)
        ]
    if status_filter:
        filtered_tickets_df = filtered_tickets_df[filtered_tickets_df["Status"].isin(
            status_filter)]
    if priority_filter:
        filtered_tickets_df = filtered_tickets_df[filtered_tickets_df["Priority"].isin(
            priority_filter)]
else:
    filtered_tickets_df = tickets_df.copy()

open_count = int(filtered_tickets_df[filtered_tickets_df["Status"].isin(
    ["Open", "In Progress", "Waiting on User"])].shape[0]) if not filtered_tickets_df.empty else 0
critical_count = int((filtered_tickets_df["Priority"] == "Critical").sum(
)) if not filtered_tickets_df.empty else 0
unassigned_count = int((filtered_tickets_df["Assignee"] == "Unassigned").sum(
)) if not filtered_tickets_df.empty else 0
resolved_count = int(filtered_tickets_df[filtered_tickets_df["Status"].isin(
    ["Resolved", "Closed"])].shape[0]) if not filtered_tickets_df.empty else 0

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Open Work", open_count, "Needs follow-up",
                "negative" if open_count > 7 else "neutral")
with metric_cols[1]:
    metric_card("Critical", critical_count, "Urgent queue",
                "negative" if critical_count else "positive")
with metric_cols[2]:
    metric_card("Unassigned", unassigned_count, "Ownership gap",
                "negative" if unassigned_count else "positive")
with metric_cols[3]:
    metric_card("Resolved", resolved_count, "Completed outcomes", "positive")

tab_create, tab_board, tab_workbench, tab_analytics = st.tabs(
    ["Create", "Board", "Workbench", "Analytics"]
)

with tab_create:
    st.markdown("#### New Ticket Intake")
    st.caption(
        "Use AI triage for automatic categorization and priority recommendations.")

    with st.form("new_ticket_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            issue_title = st.text_input(
                "Issue Title", placeholder="Data pipeline failing on stage transform")
            requester = st.text_input(
                "Requester", placeholder="name@company.com")
            assignee = st.text_input(
                "Assignee", placeholder="On-call Engineer")
            use_ai_triage = st.checkbox("Use AI triage", value=True)
        with col2:
            manual_priority = st.selectbox(
                "Manual Priority", ["Low", "Medium", "High", "Critical"], index=1)
            manual_category = st.selectbox(
                "Manual Category", ["Bug", "Feature Request", "Access", "Other"], index=0)
            manual_impact = st.selectbox(
                "Manual Impact", ["Low", "Medium", "High"], index=1)
            status = st.selectbox(
                "Initial Status", ["Open", "In Progress", "Waiting on User"], index=0)

        issue_desc = st.text_area(
            "Description",
            placeholder="Describe expected behavior, observed behavior, and business impact.",
            height=160,
        )

        submitted = st.form_submit_button(
            "Create Ticket", use_container_width=True)
        if submitted:
            if not issue_title.strip() or not issue_desc.strip():
                st.error("Please fill out both title and description.")
            else:
                triage = triage_ticket(
                    issue_title, issue_desc) if use_ai_triage else {}
                final_priority = triage.get("priority", manual_priority)
                final_category = triage.get("category", manual_category)
                final_impact = triage.get("impact", manual_impact)
                final_sentiment = triage.get("sentiment", "Neutral")
                ai_summary = triage.get("summary", "")

                session = get_session()
                try:
                    new_ticket = Ticket(
                        ticket_no=next_ticket_number(session),
                        title=issue_title.strip(),
                        description=issue_desc.strip(),
                        priority=final_priority,
                        category=final_category,
                        status=status,
                        impact=final_impact,
                        requester=requester.strip() or "Unknown",
                        assignee=assignee.strip() or "Unassigned",
                        sentiment=final_sentiment,
                        ai_summary=ai_summary,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                    session.add(new_ticket)
                    session.flush()

                    add_ticket_activity(
                        session,
                        ticket_id=new_ticket.id,
                        actor="System",
                        action="Created",
                        note="Ticket submitted through Smart Ticketing intake form.",
                    )

                    if ai_summary:
                        add_ticket_activity(
                            session,
                            ticket_id=new_ticket.id,
                            actor="AI Assistant",
                            action="Triage",
                            note=ai_summary,
                        )

                    session.commit()
                    st.success(
                        f"Created ticket {new_ticket.ticket_no} successfully.")
                    if use_ai_triage:
                        st.info(
                            f"AI triage applied: Priority={final_priority}, Category={final_category}, Impact={final_impact}, Sentiment={final_sentiment}"
                        )
                    st.rerun()
                finally:
                    session.close()

with tab_board:
    st.markdown("#### Ticket Workflow Board")
    st.caption("Visualize workload by status and quickly spot blockers.")

    board_statuses = ["Open", "In Progress", "Waiting on User", "Resolved"]
    board_cols = st.columns(len(board_statuses))

    for idx, board_status in enumerate(board_statuses):
        with board_cols[idx]:
            st.markdown(f"##### {board_status}")
            group_df = filtered_tickets_df[filtered_tickets_df["Status"] ==
                                           board_status] if not filtered_tickets_df.empty else pd.DataFrame()

            if group_df.empty:
                st.caption("No tickets")
            else:
                for _, row in group_df.head(8).iterrows():
                    st.markdown(
                        (
                            "<div class='surface-card' style='margin-bottom:0.5rem;'>"
                            f"<div style='font-weight:700'>{row['Ticket']} - {row['Title']}</div>"
                            f"<div style='margin-top:0.2rem'>{status_chip(row['Priority'])}"
                            f"{status_chip(row['Impact'])}</div>"
                            f"<div style='margin-top:0.35rem; font-size:0.84rem; color:#556274'>Assignee: {row['Assignee']}</div>"
                            "</div>"
                        ),
                        unsafe_allow_html=True,
                    )

with tab_workbench:
    st.markdown("#### Ticket Workbench")
    st.caption(
        "Update lifecycle state, assignment, and resolution notes in one place.")

    if tickets:
        option_map = {
            f"{ticket.ticket_no or f'T-{ticket.id}'} | {ticket.title}": ticket.id
            for ticket in tickets
        }
        selected_label = st.selectbox("Select Ticket", list(option_map.keys()))
        selected_id = option_map[selected_label]

        session = get_session()
        try:
            ticket_row = session.query(Ticket).filter(
                Ticket.id == selected_id).first()
            ticket_activities = (
                session.query(TicketActivity)
                .filter(TicketActivity.ticket_id == selected_id)
                .order_by(TicketActivity.created_at.desc())
                .all()
            )

            ticket = cast(Any, ticket_row)
            if ticket:
                current_status = str(ticket.status or "Open")
                current_priority = str(ticket.priority or "Medium")
                edit_col1, edit_col2 = st.columns(2)
                with edit_col1:
                    new_status = st.selectbox(
                        "Status",
                        TICKET_STATUS_OPTIONS,
                        index=TICKET_STATUS_OPTIONS.index(current_status)
                        if current_status in TICKET_STATUS_OPTIONS
                        else 0,
                        key="ticket_status_edit",
                    )
                    new_priority = st.selectbox(
                        "Priority",
                        ["Low", "Medium", "High", "Critical"],
                        index=["Low", "Medium", "High",
                               "Critical"].index(current_priority)
                        if current_priority in ["Low", "Medium", "High", "Critical"]
                        else 1,
                        key="ticket_priority_edit",
                    )
                    new_assignee = st.text_input(
                        "Assignee",
                        value=ticket.assignee or "",
                        key="ticket_assignee_edit",
                    )

                with edit_col2:
                    new_root_cause = st.text_area(
                        "Root Cause",
                        value=ticket.root_cause or "",
                        height=100,
                        key="ticket_root_cause_edit",
                    )
                    new_resolution = st.text_area(
                        "Resolution",
                        value=ticket.resolution or "",
                        height=100,
                        key="ticket_resolution_edit",
                    )
                    activity_note = st.text_input(
                        "Activity Note",
                        placeholder="Describe this update",
                        key="ticket_activity_note_edit",
                    )

                if st.button("Save Ticket Update", use_container_width=True):
                    ticket.status = str(new_status)
                    ticket.priority = str(new_priority)
                    ticket.assignee = str(new_assignee).strip() or "Unassigned"
                    ticket.root_cause = str(new_root_cause).strip()
                    ticket.resolution = str(new_resolution).strip()
                    ticket.updated_at = datetime.utcnow()

                    add_ticket_activity(
                        session,
                        ticket_id=ticket.id,
                        actor="Agent",
                        action="Updated",
                        note=activity_note.strip() or "Workflow updated from workbench.",
                    )

                    session.commit()
                    st.success(f"Updated {ticket.ticket_no}.")
                    st.rerun()

                st.markdown("##### Activity Timeline")
                if ticket_activities:
                    for raw_item in ticket_activities:
                        item = cast(Any, raw_item)
                        created_time = item.created_at
                        timestamp = created_time.strftime(
                            "%Y-%m-%d %H:%M") if created_time else "Unknown"
                        st.markdown(
                            f"- {timestamp} | {item.actor or 'System'} | {item.action} | {item.note or ''}"
                        )
                else:
                    st.caption("No activity recorded yet.")
        finally:
            session.close()
    else:
        st.info("No tickets available. Create one from the intake tab.")

with tab_analytics:
    st.markdown("#### Ticket Analytics")
    if filtered_tickets_df.empty:
        st.info("No ticket data available for analytics.")
    else:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            status_counts = filtered_tickets_df["Status"].value_counts(
            ).reset_index()
            status_counts.columns = ["Status", "Count"]
            fig_status = px.bar(
                status_counts,
                x="Status",
                y="Count",
                color="Status",
                title="Ticket Volume by Status",
                color_discrete_sequence=[
                    "#0f766e", "#ef6f38", "#0891b2", "#16a34a", "#52525b"],
            )
            fig_status.update_layout(margin=dict(l=8, r=8, t=48, b=8))
            st.plotly_chart(fig_status, use_container_width=True)

        with chart_col2:
            priority_counts = filtered_tickets_df["Priority"].value_counts(
            ).reset_index()
            priority_counts.columns = ["Priority", "Count"]
            fig_priority = px.pie(
                priority_counts,
                names="Priority",
                values="Count",
                title="Priority Mix",
                hole=0.6,
                color_discrete_sequence=["#16a34a",
                                         "#0891b2", "#f97316", "#e11d48"],
            )
            fig_priority.update_layout(margin=dict(l=8, r=8, t=48, b=8))
            st.plotly_chart(fig_priority, use_container_width=True)

        st.markdown("##### Ticket Table")
        display_df = filtered_tickets_df.copy()
        display_df["Created"] = display_df["Created"].astype(str)
        display_df["Updated"] = display_df["Updated"].astype(str)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        urgent_backlog = display_df[
            (display_df["Priority"].isin(["High", "Critical"]))
            & (display_df["Status"].isin(["Open", "In Progress", "Waiting on User"]))
        ]
        st.markdown("##### Urgent Backlog")
        if urgent_backlog.empty:
            st.success("No urgent backlog items in current scope.")
        else:
            st.dataframe(
                urgent_backlog[["Ticket", "Title", "Priority",
                                "Status", "Assignee", "Updated"]],
                use_container_width=True,
                hide_index=True,
            )
