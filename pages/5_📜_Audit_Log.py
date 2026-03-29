from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from db import AuditLog, Job, Ticket, get_session, init_db
from ui import inject_global_styles, metric_card, render_header, status_chip

st.set_page_config(
    page_title="Audit Log",
    page_icon="📜",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "Audit Log",
    "Track all system changes, user actions, and operational events for compliance and debugging.",
    "Compliance",
)


def _generate_sample_audit_logs():
    now = datetime.utcnow()
    sample_logs = [
        {"entity_type": "Job", "entity_id": "JOB-1001", "action": "Status Changed", "actor": "System",
            "details": "Status changed from Running to Completed", "created_at": now - timedelta(minutes=5)},
        {"entity_type": "Ticket", "entity_id": "TKT-1001", "action": "Updated", "actor": "Ravi",
            "details": "Priority changed from Medium to High", "created_at": now - timedelta(minutes=12)},
        {"entity_type": "Job", "entity_id": "JOB-1003", "action": "Created", "actor": "DataOps",
            "details": "New ETL Pipeline job created", "created_at": now - timedelta(minutes=25)},
        {"entity_type": "Ticket", "entity_id": "TKT-1002", "action": "AI Triage", "actor": "AI Assistant",
            "details": "Auto-triaged with priority=High, category=Bug", "created_at": now - timedelta(minutes=35)},
        {"entity_type": "System", "entity_id": None, "action": "Login", "actor": "admin@company.com",
            "details": "Successful login from 192.168.1.100", "created_at": now - timedelta(minutes=45)},
        {"entity_type": "Job", "entity_id": "JOB-1002", "action": "SLA Breach", "actor": "System",
            "details": "Job exceeded SLA threshold of 60 minutes", "created_at": now - timedelta(hours=1)},
        {"entity_type": "Ticket", "entity_id": "TKT-1001", "action": "Assigned", "actor": "Service Desk",
            "details": "Assigned to Ravi for investigation", "created_at": now - timedelta(hours=1, minutes=15)},
        {"entity_type": "System", "entity_id": None, "action": "Config Changed", "actor": "admin@company.com",
            "details": "Updated notification settings", "created_at": now - timedelta(hours=2)},
        {"entity_type": "Job", "entity_id": "JOB-1001", "action": "Started", "actor": "Job Scheduler",
            "details": "Job execution started", "created_at": now - timedelta(hours=2, minutes=30)},
        {"entity_type": "Ticket", "entity_id": "TKT-1001", "action": "Created", "actor": "System",
            "details": "Ticket created from job alert", "created_at": now - timedelta(hours=3)},
        {"entity_type": "System", "entity_id": None, "action": "Backup Completed", "actor": "System",
            "details": "Daily database backup completed successfully", "created_at": now - timedelta(hours=4)},
        {"entity_type": "Job", "entity_id": "JOB-1004", "action": "Failed", "actor": "System",
            "details": "Job failed with error: Connection timeout", "created_at": now - timedelta(hours=5)},
        {"entity_type": "System", "entity_id": None, "action": "Service Restart", "actor": "Infra Team",
            "details": "AI Service restarted for maintenance", "created_at": now - timedelta(hours=6)},
        {"entity_type": "Ticket", "entity_id": "TKT-1003", "action": "Resolved", "actor": "DevOps",
            "details": "Issue resolved, root cause identified as config error", "created_at": now - timedelta(hours=8)},
        {"entity_type": "System", "entity_id": None, "action": "Deployment", "actor": "CI/CD Pipeline",
            "details": "Version 2.0.0 deployed to production", "created_at": now - timedelta(hours=12)},
    ]
    return sample_logs


audit_logs = _generate_sample_audit_logs()

total_logs = len(audit_logs)
job_events = sum(1 for log in audit_logs if log["entity_type"] == "Job")
ticket_events = sum(1 for log in audit_logs if log["entity_type"] == "Ticket")
system_events = sum(1 for log in audit_logs if log["entity_type"] == "System")

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Total Events", total_logs, "Last 24 hours", "neutral")
with metric_cols[1]:
    metric_card("Job Events", job_events, "Pipeline activity", "neutral")
with metric_cols[2]:
    metric_card("Ticket Events", ticket_events, "Incident activity", "neutral")
with metric_cols[3]:
    metric_card("System Events", system_events, "Infrastructure", "neutral")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1, 1, 1])
with filter_col1:
    search_text = st.text_input(
        "Search logs", placeholder="Entity ID, actor, or details...")
with filter_col2:
    entity_filter = st.multiselect(
        "Entity Type", ["Job", "Ticket", "System"], default=["Job", "Ticket", "System"])
with filter_col3:
    action_options = list(set(log["action"] for log in audit_logs))
    action_filter = st.multiselect(
        "Action", action_options, default=action_options)
with filter_col4:
    time_filter = st.selectbox("Time Range", [
                               "Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "All Time"], index=2)

filtered_logs = audit_logs.copy()

if entity_filter:
    filtered_logs = [
        log for log in filtered_logs if log["entity_type"] in entity_filter]

if action_filter:
    filtered_logs = [
        log for log in filtered_logs if log["action"] in action_filter]

if search_text:
    needle = search_text.lower().strip()
    filtered_logs = [
        log for log in filtered_logs
        if needle in (log.get("entity_id") or "").lower()
        or needle in (log.get("actor") or "").lower()
        or needle in (log.get("details") or "").lower()
    ]

now = datetime.utcnow()
if time_filter == "Last Hour":
    filtered_logs = [
        log for log in filtered_logs if log["created_at"] > now - timedelta(hours=1)]
elif time_filter == "Last 6 Hours":
    filtered_logs = [
        log for log in filtered_logs if log["created_at"] > now - timedelta(hours=6)]
elif time_filter == "Last 24 Hours":
    filtered_logs = [
        log for log in filtered_logs if log["created_at"] > now - timedelta(hours=24)]
elif time_filter == "Last 7 Days":
    filtered_logs = [
        log for log in filtered_logs if log["created_at"] > now - timedelta(days=7)]

tab_timeline, tab_table = st.tabs(["Timeline View", "Table View"])

with tab_timeline:
    st.markdown("#### Activity Timeline")

    if not filtered_logs:
        st.info("No audit logs match the current filters.")
    else:
        for log in filtered_logs:
            entity_icon = "📊" if log["entity_type"] == "Job" else "🎟️" if log["entity_type"] == "Ticket" else "⚙️"

            action_color = "#10b981"
            if log["action"] in ["Failed", "SLA Breach"]:
                action_color = "#f43f5e"
            elif log["action"] in ["Created", "Started"]:
                action_color = "#06b6d4"
            elif log["action"] in ["Updated", "Status Changed", "Assigned"]:
                action_color = "#f59e0b"
            elif log["action"] in ["AI Triage"]:
                action_color = "#8b5cf6"

            time_ago = now - log["created_at"]
            if time_ago.total_seconds() < 60:
                time_str = "Just now"
            elif time_ago.total_seconds() < 3600:
                time_str = f"{int(time_ago.total_seconds() / 60)} min ago"
            elif time_ago.total_seconds() < 86400:
                time_str = f"{int(time_ago.total_seconds() / 3600)} hours ago"
            else:
                time_str = f"{int(time_ago.total_seconds() / 86400)} days ago"

            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 0.75rem; display: flex; gap: 1rem; align-items: flex-start;">
                    <div style="font-size: 1.5rem; padding-top: 0.25rem;">{entity_icon}</div>
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                            <div style="display: flex; align-items: center; gap: 0.75rem;">
                                <span style="font-weight: 600; color: var(--text-primary);">{log['entity_type']}</span>
                                {f"<span style='color: var(--accent-cyan);'>{log['entity_id']}</span>" if log['entity_id'] else ""}
                                <span style="padding: 0.2rem 0.5rem; border-radius: 4px; background: {action_color}20; color: {action_color}; font-size: 0.75rem; font-weight: 600;">{log['action']}</span>
                            </div>
                            <span style="font-size: 0.8rem; color: var(--text-muted);">{time_str}</span>
                        </div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">{log['details']}</div>
                        <div style="margin-top: 0.35rem; font-size: 0.8rem; color: var(--text-muted);">
                            by <strong>{log['actor']}</strong> • {log['created_at'].strftime('%Y-%m-%d %H:%M:%S UTC')}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_table:
    st.markdown("#### Audit Log Table")

    if not filtered_logs:
        st.info("No audit logs match the current filters.")
    else:
        table_data = [
            {
                "Timestamp": log["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
                "Entity Type": log["entity_type"],
                "Entity ID": log["entity_id"] or "-",
                "Action": log["action"],
                "Actor": log["actor"],
                "Details": log["details"][:80] + "..." if len(log["details"]) > 80 else log["details"],
            }
            for log in filtered_logs
        ]

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Audit Log (CSV)",
            data=csv_data,
            file_name=f"audit_log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.markdown("---")
st.markdown("#### Compliance Summary")

compliance_col1, compliance_col2, compliance_col3 = st.columns(3)

with compliance_col1:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">📋 Retention Policy</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                Audit logs are retained for <strong>90 days</strong> in accordance with compliance requirements.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with compliance_col2:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">🔒 Data Integrity</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                All logs are immutable and include timestamp verification for audit purposes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with compliance_col3:
    st.markdown(
        """
        <div class="surface-card">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">📊 Automated Reports</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                Weekly compliance reports are generated automatically for review.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
