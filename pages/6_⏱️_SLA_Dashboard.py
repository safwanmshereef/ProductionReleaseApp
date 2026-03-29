from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import Job, Ticket, get_session, init_db
from ui import inject_global_styles, metric_card, render_header, status_chip

st.set_page_config(
    page_title="SLA Dashboard",
    page_icon="⏱️",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "SLA Dashboard",
    "Monitor service level agreements, track compliance, and identify at-risk workloads.",
    "SLA Intelligence",
)

session = get_session()
try:
    jobs = session.query(Job).order_by(Job.created_at.desc()).all()
finally:
    session.close()


def _calculate_sla_status(job):
    if not job.sla_min or job.sla_min <= 0:
        return "No SLA", 0, 0

    duration = job.duration_min or 0
    sla = job.sla_min

    percent_used = (duration / sla) * 100 if sla > 0 else 0
    time_remaining = sla - duration

    if job.status in ["Completed", "Failed"]:
        if duration > sla:
            return "Breached", percent_used, time_remaining
        else:
            return "Met", percent_used, time_remaining
    elif job.status == "Running":
        if duration >= sla:
            return "Breached", percent_used, time_remaining
        elif percent_used >= 80:
            return "At Risk", percent_used, time_remaining
        else:
            return "On Track", percent_used, time_remaining
    else:
        return "Pending", 0, sla


sla_data = []
for job in jobs:
    status, percent_used, time_remaining = _calculate_sla_status(job)
    sla_data.append({
        "job": job,
        "sla_status": status,
        "percent_used": percent_used,
        "time_remaining": time_remaining,
    })

total_jobs = len(sla_data)
met_count = sum(1 for d in sla_data if d["sla_status"] == "Met")
breached_count = sum(1 for d in sla_data if d["sla_status"] == "Breached")
at_risk_count = sum(1 for d in sla_data if d["sla_status"] == "At Risk")
on_track_count = sum(1 for d in sla_data if d["sla_status"] == "On Track")

compliance_rate = round((met_count / (met_count + breached_count))
                        * 100, 1) if (met_count + breached_count) > 0 else 100

metric_cols = st.columns(5)
with metric_cols[0]:
    tone = "positive" if compliance_rate >= 95 else "negative" if compliance_rate < 80 else "neutral"
    metric_card("SLA Compliance", f"{compliance_rate}%", "Overall rate", tone)
with metric_cols[1]:
    metric_card("SLA Met", met_count, "Completed on time", "positive")
with metric_cols[2]:
    metric_card("SLA Breached", breached_count, "Exceeded threshold",
                "negative" if breached_count > 0 else "positive")
with metric_cols[3]:
    metric_card("At Risk", at_risk_count, ">80% SLA consumed",
                "negative" if at_risk_count > 0 else "neutral")
with metric_cols[4]:
    metric_card("On Track", on_track_count, "Running smoothly",
                "positive" if on_track_count > 0 else "neutral")

tab_overview, tab_active, tab_breaches, tab_trends = st.tabs(
    ["Overview", "Active SLAs", "Breaches", "Trends"]
)

with tab_overview:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### SLA Status Distribution")
        status_counts = {
            "Met": met_count,
            "Breached": breached_count,
            "At Risk": at_risk_count,
            "On Track": on_track_count,
        }
        status_counts = {k: v for k, v in status_counts.items() if v > 0}

        if status_counts:
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                hole=0.6,
                color=list(status_counts.keys()),
                color_discrete_map={
                    "Met": "#10b981",
                    "Breached": "#f43f5e",
                    "At Risk": "#f59e0b",
                    "On Track": "#06b6d4",
                },
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No SLA data available for visualization.")

    with chart_col2:
        st.markdown("#### SLA by Priority")
        priority_sla = {}
        for d in sla_data:
            priority = d["job"].priority or "Medium"
            if priority not in priority_sla:
                priority_sla[priority] = {"met": 0, "breached": 0}
            if d["sla_status"] == "Met":
                priority_sla[priority]["met"] += 1
            elif d["sla_status"] == "Breached":
                priority_sla[priority]["breached"] += 1

        if priority_sla:
            priorities = list(priority_sla.keys())
            met_vals = [priority_sla[p]["met"] for p in priorities]
            breached_vals = [priority_sla[p]["breached"] for p in priorities]

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Met", x=priorities,
                          y=met_vals, marker_color="#10b981"))
            fig.add_trace(go.Bar(name="Breached", x=priorities,
                          y=breached_vals, marker_color="#f43f5e"))
            fig.update_layout(
                barmode="stack",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No priority data available.")

    st.markdown("#### SLA Compliance Gauge")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=compliance_rate,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Overall SLA Compliance",
               "font": {"size": 20, "color": "#f8fafc"}},
        delta={"reference": 95, "increasing": {"color": "#10b981"},
               "decreasing": {"color": "#f43f5e"}},
        number={"font": {"size": 48, "color": "#f8fafc"}, "suffix": "%"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748b"},
            "bar": {"color": "#8b5cf6"},
            "bgcolor": "rgba(255,255,255,0.05)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 70], "color": "rgba(244, 63, 94, 0.2)"},
                {"range": [70, 90], "color": "rgba(245, 158, 11, 0.2)"},
                {"range": [90, 100], "color": "rgba(16, 185, 129, 0.2)"},
            ],
            "threshold": {
                "line": {"color": "#10b981", "width": 4},
                "thickness": 0.75,
                "value": 95,
            },
        },
    ))

    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        height=300,
        margin=dict(l=30, r=30, t=50, b=30),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with tab_active:
    st.markdown("#### Active SLA Monitoring")

    active_sla = [d for d in sla_data if d["job"].status == "Running"]

    if not active_sla:
        st.info("No jobs are currently running with active SLAs.")
    else:
        active_sla.sort(key=lambda x: x["percent_used"], reverse=True)

        for item in active_sla:
            job = item["job"]
            percent = min(item["percent_used"], 100)
            time_left = item["time_remaining"]

            if item["sla_status"] == "Breached":
                bar_color = "#f43f5e"
                status_color = "#f43f5e"
            elif item["sla_status"] == "At Risk":
                bar_color = "#f59e0b"
                status_color = "#f59e0b"
            else:
                bar_color = "#10b981"
                status_color = "#10b981"

            time_display = f"{abs(time_left)} min {'over' if time_left < 0 else 'remaining'}"

            st.markdown(
                f"""
                <div class="surface-card" style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <div>
                            <span style="font-weight: 700; color: var(--text-primary); font-size: 1.1rem;">{job.job_id}</span>
                            <span style="color: var(--text-muted); margin-left: 0.75rem;">{job.job_type}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            {status_chip(item['sla_status'])}
                            <span style="color: {status_color}; font-weight: 600;">{time_display}</span>
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border-radius: 8px; height: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {bar_color}, {bar_color}88); width: {min(percent, 100)}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted);">
                        <span>Duration: {job.duration_min} min</span>
                        <span>{percent:.1f}% of SLA ({job.sla_min} min)</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_breaches:
    st.markdown("#### SLA Breaches")

    breached_items = [d for d in sla_data if d["sla_status"] == "Breached"]

    if not breached_items:
        st.success("🎉 No SLA breaches! All jobs are meeting their targets.")
    else:
        breach_col1, breach_col2 = st.columns([2, 1])

        with breach_col1:
            breach_table = []
            for item in breached_items:
                job = item["job"]
                overage = (job.duration_min or 0) - (job.sla_min or 0)
                breach_table.append({
                    "Job ID": job.job_id,
                    "Type": job.job_type,
                    "Owner": job.owner or "Unassigned",
                    "Duration": f"{job.duration_min} min",
                    "SLA": f"{job.sla_min} min",
                    "Overage": f"+{overage} min",
                    "Status": job.status,
                })

            df = pd.DataFrame(breach_table)
            st.dataframe(df, use_container_width=True, hide_index=True)

        with breach_col2:
            st.markdown("##### Breach Analysis")

            type_breaches = {}
            for item in breached_items:
                job_type = item["job"].job_type or "Unknown"
                type_breaches[job_type] = type_breaches.get(job_type, 0) + 1

            if type_breaches:
                fig = px.bar(
                    x=list(type_breaches.keys()),
                    y=list(type_breaches.values()),
                    color=list(type_breaches.values()),
                    color_continuous_scale=["#f43f5e", "#dc2626"],
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#94a3b8"),
                    yaxis=dict(title="Breaches",
                               gridcolor="rgba(255,255,255,0.05)"),
                    xaxis=dict(title="", gridcolor="rgba(255,255,255,0.05)"),
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=200,
                    showlegend=False,
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig, use_container_width=True)

with tab_trends:
    st.markdown("#### SLA Trends (Simulated Historical Data)")

    now = datetime.utcnow()
    days = [(now - timedelta(days=i)).strftime("%m/%d")
            for i in range(14, 0, -1)]

    import random
    compliance_history = [random.uniform(85, 99) for _ in range(14)]
    breaches_history = [random.randint(0, 3) for _ in range(14)]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=days,
        y=compliance_history,
        mode="lines+markers",
        name="Compliance %",
        line=dict(color="#8b5cf6", width=3),
        marker=dict(size=8),
    ))
    fig_trend.add_hline(y=95, line_dash="dash",
                        line_color="#10b981", annotation_text="Target (95%)")
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        yaxis=dict(title="Compliance %", range=[
                   80, 100], gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(title="Date", gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(l=20, r=20, t=40, b=40),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("#### Daily Breach Count")
    fig_breaches = go.Figure()
    fig_breaches.add_trace(go.Bar(
        x=days,
        y=breaches_history,
        marker_color=["#f43f5e" if b > 1 else "#f59e0b" if b >
                      0 else "#10b981" for b in breaches_history],
    ))
    fig_breaches.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        yaxis=dict(title="Breaches", gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(title="Date", gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(l=20, r=20, t=20, b=40),
        height=200,
    )
    st.plotly_chart(fig_breaches, use_container_width=True)
