from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from db import JOB_PRIORITY_OPTIONS, JOB_STATUS_OPTIONS, Job, get_session, init_db
from ui import inject_global_styles, metric_card, render_header

st.set_page_config(
    page_title="Job Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "Job Monitoring Dashboard",
    "Track SLA health, execution trends, and workflow status in real time.",
    "Runtime Intelligence",
)


def _fetch_jobs():
    session = get_session()
    try:
        return session.query(Job).order_by(Job.created_at.desc()).all()
    finally:
        session.close()


def _next_job_id(jobs):
    max_num = 1000
    for job in jobs:
        if not job.job_id:
            continue
        if job.job_id.startswith("JOB-"):
            suffix = job.job_id.replace("JOB-", "", 1)
            if suffix.isdigit():
                max_num = max(max_num, int(suffix))
    return f"JOB-{max_num + 1}"


jobs = _fetch_jobs()

if jobs:
    df = pd.DataFrame(
        [
            {
                "Job ID": job.job_id,
                "Type": job.job_type,
                "Owner": job.owner or "Unassigned",
                "Status": job.status,
                "Priority": job.priority or "Medium",
                "Duration (min)": int(job.duration_min or 0),
                "SLA (min)": int(job.sla_min or 0),
                "SLA Breach": "Yes"
                if (job.duration_min or 0) > (job.sla_min or 0) and (job.status or "") in {"Running", "Completed", "Failed"}
                else "No",
                "Heartbeat": job.last_heartbeat,
                "Created": job.created_at,
                "Notes": job.notes or "",
            }
            for job in jobs
        ]
    )
else:
    df = pd.DataFrame(
        columns=[
            "Job ID",
            "Type",
            "Owner",
            "Status",
            "Priority",
            "Duration (min)",
            "SLA (min)",
            "SLA Breach",
            "Heartbeat",
            "Created",
            "Notes",
        ]
    )

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.2, 1, 1, 1])
with filter_col1:
    search_job = st.text_input(
        "Search Job ID or Type", placeholder="JOB-1001, ETL")
with filter_col2:
    selected_status = st.multiselect(
        "Status", JOB_STATUS_OPTIONS, default=JOB_STATUS_OPTIONS)
with filter_col3:
    selected_priority = st.multiselect(
        "Priority", JOB_PRIORITY_OPTIONS, default=JOB_PRIORITY_OPTIONS)
with filter_col4:
    selected_owner = st.multiselect(
        "Owner",
        sorted(df["Owner"].dropna().unique().tolist()) if not df.empty else [],
        default=sorted(df["Owner"].dropna().unique().tolist()
                       ) if not df.empty else [],
    )

filtered_df = df.copy()
if not filtered_df.empty:
    if search_job:
        needle = search_job.strip().lower()
        filtered_df = filtered_df[
            filtered_df["Job ID"].str.lower().str.contains(needle)
            | filtered_df["Type"].str.lower().str.contains(needle)
        ]
    if selected_status:
        filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]
    if selected_priority:
        filtered_df = filtered_df[filtered_df["Priority"].isin(
            selected_priority)]
    if selected_owner:
        filtered_df = filtered_df[filtered_df["Owner"].isin(selected_owner)]

total_jobs = int(filtered_df.shape[0])
running_jobs = int(
    (filtered_df["Status"] == "Running").sum()) if not filtered_df.empty else 0
failed_jobs = int(
    (filtered_df["Status"] == "Failed").sum()) if not filtered_df.empty else 0
breaches = int((filtered_df["SLA Breach"] == "Yes").sum()
               ) if not filtered_df.empty else 0
avg_duration = round(
    filtered_df["Duration (min)"].mean(), 1) if not filtered_df.empty else 0
success_rate = round(((total_jobs - failed_jobs) / total_jobs)
                     * 100, 1) if total_jobs > 0 else 0

metric_cols = st.columns(5)
with metric_cols[0]:
    metric_card("Total Jobs", total_jobs, "Filtered scope", "neutral")
with metric_cols[1]:
    metric_card("Running", running_jobs, "Active now",
                "positive" if running_jobs else "neutral")
with metric_cols[2]:
    metric_card("Failed", failed_jobs, "Needs investigation",
                "negative" if failed_jobs else "positive")
with metric_cols[3]:
    metric_card("SLA Breaches", breaches, "Threshold exceeded",
                "negative" if breaches else "positive")
with metric_cols[4]:
    metric_card("Success Rate", f"{success_rate}%",
                f"Avg duration {avg_duration} min", "neutral")

tab_overview, tab_manage, tab_data = st.tabs(
    ["Overview", "Manage Jobs", "Data"])

with tab_overview:
    chart_col1, chart_col2 = st.columns([1, 1])
    with chart_col1:
        if not filtered_df.empty:
            status_counts = filtered_df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig_status = px.pie(
                status_counts,
                names="Status",
                values="Count",
                title="Job Status Distribution",
                hole=0.56,
                color_discrete_sequence=[
                    "#0f766e", "#ef6f38", "#0891b2", "#e11d48", "#f97316"],
            )
            fig_status.update_layout(margin=dict(l=8, r=8, t=50, b=8))
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No jobs available for charting.")

    with chart_col2:
        if not filtered_df.empty:
            duration_by_type = (
                filtered_df.groupby("Type", as_index=False)["Duration (min)"].mean(
                ).sort_values("Duration (min)", ascending=False)
            )
            fig_duration = px.bar(
                duration_by_type,
                x="Type",
                y="Duration (min)",
                color="Duration (min)",
                title="Average Duration by Job Type",
                color_continuous_scale=["#d1fae5",
                                        "#5eead4", "#14b8a6", "#0f766e"],
            )
            fig_duration.update_layout(margin=dict(
                l=8, r=8, t=50, b=8), xaxis_title="", yaxis_title="Minutes")
            st.plotly_chart(fig_duration, use_container_width=True)
        else:
            st.info("No duration trends available yet.")

    st.markdown("#### SLA Breach Queue")
    breach_df = filtered_df[filtered_df["SLA Breach"] ==
                            "Yes"] if not filtered_df.empty else pd.DataFrame()
    if not breach_df.empty:
        st.dataframe(
            breach_df[["Job ID", "Type", "Owner", "Status",
                       "Duration (min)", "SLA (min)", "Notes"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No SLA breaches in the current filter scope.")

with tab_manage:
    form_col1, form_col2 = st.columns(2)

    with form_col1:
        st.markdown("#### Create Job")
        with st.form("create_job_form", clear_on_submit=True):
            job_type = st.text_input("Job Type", placeholder="ETL Pipeline")
            owner = st.text_input("Owner", placeholder="DataOps")
            priority = st.selectbox("Priority", JOB_PRIORITY_OPTIONS, index=1)
            sla_min = st.number_input(
                "SLA Threshold (min)", min_value=5, max_value=1000, value=60, step=5)
            notes = st.text_area(
                "Notes", placeholder="Optional runbook details")

            submit_job = st.form_submit_button("Create Job")
            if submit_job:
                if not job_type.strip():
                    st.error("Job type is required.")
                else:
                    session = get_session()
                    try:
                        current_jobs = session.query(Job).all()
                        new_job = Job(
                            job_id=_next_job_id(current_jobs),
                            job_type=job_type.strip(),
                            owner=owner.strip() or "Unassigned",
                            status="Queued",
                            priority=priority,
                            duration_min=0,
                            sla_min=int(sla_min),
                            notes=notes.strip(),
                            created_at=datetime.utcnow(),
                            last_heartbeat=datetime.utcnow(),
                        )
                        session.add(new_job)
                        session.commit()
                        st.success(f"Created {new_job.job_id} successfully.")
                        st.rerun()
                    finally:
                        session.close()

    with form_col2:
        st.markdown("#### Update Job")
        if jobs:
            options = {
                f"{job.job_id} | {job.job_type} | {job.status}": job.id
                for job in jobs
            }
            selected_label = st.selectbox("Select Job", list(options.keys()))
            selected_id = options[selected_label]
            selected_job = next(
                (job for job in jobs if job.id == selected_id), None)

            new_status = st.selectbox("New Status", JOB_STATUS_OPTIONS, index=JOB_STATUS_OPTIONS.index(
                selected_job.status) if selected_job and selected_job.status in JOB_STATUS_OPTIONS else 0)
            new_duration = st.number_input(
                "Duration (min)",
                min_value=0,
                max_value=10000,
                value=int(selected_job.duration_min or 0) if selected_job else 0,
                step=1,
            )
            append_note = st.text_input(
                "Add Note", placeholder="What changed?")

            if st.button("Save Job Update", use_container_width=True):
                session = get_session()
                try:
                    job = session.query(Job).filter(
                        Job.id == selected_id).first()
                    if job:
                        now = datetime.utcnow()
                        job.status = new_status
                        job.duration_min = int(new_duration)
                        job.last_heartbeat = now
                        if new_status == "Running" and not job.started_at:
                            job.started_at = now
                        if new_status in {"Completed", "Failed"}:
                            job.ended_at = now
                        if append_note.strip():
                            base_note = f"{job.notes}\n" if job.notes else ""
                            job.notes = f"{base_note}[{now.strftime('%Y-%m-%d %H:%M')}] {append_note.strip()}"
                        session.commit()
                        st.success(f"Updated {job.job_id}.")
                        st.rerun()
                finally:
                    session.close()
        else:
            st.info("Create your first job to start managing workflows.")

    st.markdown("#### Simulation")
    if st.button("Advance Running Jobs by 5 Minutes", use_container_width=True):
        session = get_session()
        try:
            running_list = session.query(Job).filter(
                Job.status == "Running").all()
            now = datetime.utcnow()
            for item in running_list:
                item.duration_min = int(item.duration_min or 0) + 5
                item.last_heartbeat = now
            session.commit()
            st.success(f"Updated {len(running_list)} running jobs.")
            st.rerun()
        finally:
            session.close()

with tab_data:
    st.markdown("#### Job Inventory")
    if filtered_df.empty:
        st.info("No jobs available in this filter scope.")
    else:
        export_df = filtered_df.copy()
        export_df["Created"] = export_df["Created"].astype(str)
        export_df["Heartbeat"] = export_df["Heartbeat"].astype(str)

        st.dataframe(export_df, use_container_width=True, hide_index=True)
        csv_data = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="job_monitoring_export.csv",
            mime="text/csv",
            use_container_width=True,
        )
