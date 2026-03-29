import platform
import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import Job, SystemMetric, Ticket, get_session, init_db, record_system_metric
from ui import inject_global_styles, metric_card, render_header, status_chip

st.set_page_config(
    page_title="System Health Monitor",
    page_icon="💓",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "System Health Monitor",
    "Real-time system performance metrics, uptime tracking, and infrastructure health.",
    "Infrastructure",
)


def _get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version()[:50] if platform.version() else "Unknown",
        "python_version": platform.python_version(),
        "processor": platform.processor()[:40] if platform.processor() else "Unknown",
        "machine": platform.machine(),
    }


def _simulate_metrics():
    return {
        "cpu_percent": round(random.uniform(15, 85), 1),
        "memory_percent": round(random.uniform(40, 75), 1),
        "disk_percent": round(random.uniform(30, 70), 1),
        "network_in_mbps": round(random.uniform(10, 150), 2),
        "network_out_mbps": round(random.uniform(5, 80), 2),
        "active_connections": random.randint(50, 500),
        "response_time_ms": round(random.uniform(20, 200), 1),
        "error_rate_percent": round(random.uniform(0, 2.5), 2),
    }


def _get_service_status():
    return [
        {"name": "Database", "status": "Healthy",
            "latency": f"{random.randint(1, 15)}ms", "uptime": "99.99%"},
        {"name": "API Gateway", "status": "Healthy",
            "latency": f"{random.randint(10, 50)}ms", "uptime": "99.95%"},
        {"name": "Job Scheduler", "status": "Healthy",
            "latency": f"{random.randint(5, 30)}ms", "uptime": "99.97%"},
        {"name": "AI Service", "status": "Healthy" if random.random(
        ) > 0.1 else "Degraded", "latency": f"{random.randint(100, 500)}ms", "uptime": "99.80%"},
        {"name": "Notification Service", "status": "Healthy",
            "latency": f"{random.randint(20, 100)}ms", "uptime": "99.92%"},
        {"name": "Cache Layer", "status": "Healthy",
            "latency": f"{random.randint(1, 10)}ms", "uptime": "99.99%"},
    ]


metrics = _simulate_metrics()
system_info = _get_system_info()
services = _get_service_status()

session = get_session()
try:
    total_jobs = session.query(Job).count()
    running_jobs = session.query(Job).filter(Job.status == "Running").count()
    failed_jobs = session.query(Job).filter(Job.status == "Failed").count()
    open_tickets = session.query(Ticket).filter(
        Ticket.status.in_(["Open", "In Progress"])).count()
finally:
    session.close()

overall_health = "Healthy"
health_score = 100
if metrics["cpu_percent"] > 80:
    health_score -= 15
if metrics["memory_percent"] > 80:
    health_score -= 15
if metrics["error_rate_percent"] > 1:
    health_score -= 20
if failed_jobs > 2:
    health_score -= 10
degraded_services = sum(1 for s in services if s["status"] != "Healthy")
health_score -= degraded_services * 5

if health_score < 70:
    overall_health = "Critical"
elif health_score < 85:
    overall_health = "Degraded"

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
        <div style="font-size: 0.9rem; color: var(--text-secondary);">System Status:</div>
        {status_chip(overall_health)}
        <div style="font-size: 0.9rem; color: var(--text-muted);">Health Score: <strong style="color: var(--text-primary);">{health_score}%</strong></div>
        <div style="font-size: 0.9rem; color: var(--text-muted);">Last Updated: <strong style="color: var(--text-primary);">{datetime.utcnow().strftime('%H:%M:%S UTC')}</strong></div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(6)
with metric_cols[0]:
    tone = "negative" if metrics["cpu_percent"] > 80 else "positive" if metrics["cpu_percent"] < 50 else "neutral"
    metric_card(
        "CPU Usage", f"{metrics['cpu_percent']}%", "Current load", tone)
with metric_cols[1]:
    tone = "negative" if metrics["memory_percent"] > 80 else "positive" if metrics["memory_percent"] < 60 else "neutral"
    metric_card(
        "Memory", f"{metrics['memory_percent']}%", "RAM utilization", tone)
with metric_cols[2]:
    tone = "negative" if metrics["disk_percent"] > 85 else "neutral"
    metric_card("Disk Usage", f"{metrics['disk_percent']}%", "Storage", tone)
with metric_cols[3]:
    tone = "negative" if metrics["response_time_ms"] > 150 else "positive" if metrics["response_time_ms"] < 50 else "neutral"
    metric_card("Response Time",
                f"{metrics['response_time_ms']}ms", "Avg latency", tone)
with metric_cols[4]:
    tone = "negative" if metrics["error_rate_percent"] > 1 else "positive"
    metric_card(
        "Error Rate", f"{metrics['error_rate_percent']}%", "Request errors", tone)
with metric_cols[5]:
    metric_card("Connections",
                metrics["active_connections"], "Active sessions", "neutral")

tab_overview, tab_services, tab_performance, tab_system = st.tabs(
    ["Overview", "Services", "Performance", "System Info"]
)

with tab_overview:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### Resource Utilization")
        fig = go.Figure()

        categories = ["CPU", "Memory", "Disk", "Network"]
        values = [
            metrics["cpu_percent"],
            metrics["memory_percent"],
            metrics["disk_percent"],
            min((metrics["network_in_mbps"] / 200) * 100, 100),
        ]
        colors = ["#8b5cf6", "#06b6d4", "#10b981", "#f59e0b"]

        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}%" for v in values],
            textposition="outside",
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.05)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.markdown("#### Application Metrics")
        app_metrics = [
            {"Metric": "Total Jobs", "Value": total_jobs, "Status": "Normal"},
            {"Metric": "Running Jobs", "Value": running_jobs,
                "Status": "Active" if running_jobs > 0 else "Idle"},
            {"Metric": "Failed Jobs", "Value": failed_jobs,
                "Status": "Alert" if failed_jobs > 0 else "OK"},
            {"Metric": "Open Tickets", "Value": open_tickets,
                "Status": "Attention" if open_tickets > 5 else "Normal"},
            {"Metric": "Active Connections",
                "Value": metrics["active_connections"], "Status": "Normal"},
        ]
        app_df = pd.DataFrame(app_metrics)
        st.dataframe(app_df, use_container_width=True, hide_index=True)

    st.markdown("#### Network Throughput")

    now = datetime.utcnow()
    time_points = [(now - timedelta(minutes=i)).strftime("%H:%M")
                   for i in range(30, 0, -1)]

    network_in = [metrics["network_in_mbps"] +
                  random.uniform(-30, 30) for _ in range(30)]
    network_out = [metrics["network_out_mbps"] +
                   random.uniform(-20, 20) for _ in range(30)]

    fig_network = go.Figure()
    fig_network.add_trace(go.Scatter(
        x=time_points, y=network_in, mode="lines", name="Inbound",
        line=dict(color="#06b6d4", width=2),
        fill="tozeroy", fillcolor="rgba(6, 182, 212, 0.1)",
    ))
    fig_network.add_trace(go.Scatter(
        x=time_points, y=network_out, mode="lines", name="Outbound",
        line=dict(color="#8b5cf6", width=2),
        fill="tozeroy", fillcolor="rgba(139, 92, 246, 0.1)",
    ))
    fig_network.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        yaxis=dict(title="Mbps", gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250,
    )
    st.plotly_chart(fig_network, use_container_width=True)

with tab_services:
    st.markdown("#### Service Health Status")

    for service in services:
        status_color = "#10b981" if service["status"] == "Healthy" else "#f59e0b" if service["status"] == "Degraded" else "#f43f5e"
        st.markdown(
            f"""
            <div class="surface-card" style="margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color}; box-shadow: 0 0 10px {status_color};"></div>
                    <div>
                        <div style="font-weight: 600; color: var(--text-primary);">{service['name']}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Uptime: {service['uptime']}</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 2rem;">
                    <div style="text-align: right;">
                        <div style="font-size: 0.75rem; color: var(--text-muted);">Latency</div>
                        <div style="font-weight: 600; color: var(--text-primary);">{service['latency']}</div>
                    </div>
                    {status_chip(service['status'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Service Dependencies")
    st.markdown(
        """
        ```
        ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
        │   Client    │────►│ API Gateway │────►│  Database   │
        └─────────────┘     └──────┬──────┘     └─────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
             ┌────────────┐ ┌────────────┐ ┌────────────┐
             │Job Scheduler│ │ AI Service │ │Cache Layer │
             └────────────┘ └────────────┘ └────────────┘
        ```
        """,
    )

with tab_performance:
    st.markdown("#### Performance Trends (Last 60 Minutes)")

    now = datetime.utcnow()
    time_points = [(now - timedelta(minutes=i)).strftime("%H:%M")
                   for i in range(60, 0, -1)]

    cpu_history = [max(10, min(95, metrics["cpu_percent"] +
                       random.uniform(-20, 20))) for _ in range(60)]
    memory_history = [max(30, min(
        90, metrics["memory_percent"] + random.uniform(-15, 15))) for _ in range(60)]
    response_history = [max(10, min(
        300, metrics["response_time_ms"] + random.uniform(-50, 50))) for _ in range(60)]

    fig_perf = go.Figure()
    fig_perf.add_trace(go.Scatter(
        x=time_points, y=cpu_history, mode="lines", name="CPU %",
        line=dict(color="#8b5cf6", width=2),
    ))
    fig_perf.add_trace(go.Scatter(
        x=time_points, y=memory_history, mode="lines", name="Memory %",
        line=dict(color="#06b6d4", width=2),
    ))
    fig_perf.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        yaxis=dict(title="Percentage", gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
    )
    st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("#### Response Time Distribution")
    fig_response = go.Figure()
    fig_response.add_trace(go.Scatter(
        x=time_points, y=response_history, mode="lines", name="Response Time",
        line=dict(color="#10b981", width=2),
        fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.1)",
    ))
    fig_response.add_hline(y=100, line_dash="dash",
                           line_color="#f59e0b", annotation_text="Warning Threshold")
    fig_response.add_hline(y=200, line_dash="dash",
                           line_color="#f43f5e", annotation_text="Critical Threshold")
    fig_response.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        yaxis=dict(title="Milliseconds", gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(l=20, r=20, t=20, b=20),
        height=250,
    )
    st.plotly_chart(fig_response, use_container_width=True)

with tab_system:
    st.markdown("#### System Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.markdown("##### Environment")
        env_data = [
            {"Property": "Operating System", "Value": system_info["os"]},
            {"Property": "OS Version", "Value": system_info["os_version"]},
            {"Property": "Python Version",
                "Value": system_info["python_version"]},
            {"Property": "Machine Type", "Value": system_info["machine"]},
            {"Property": "Processor", "Value": system_info["processor"]},
        ]
        st.dataframe(pd.DataFrame(env_data),
                     use_container_width=True, hide_index=True)

    with info_col2:
        st.markdown("##### Application")
        app_data = [
            {"Property": "App Name", "Value": "Enterprise Ops Hub"},
            {"Property": "Version", "Value": "2.0.0"},
            {"Property": "Framework", "Value": "Streamlit"},
            {"Property": "Database", "Value": "SQLite"},
            {"Property": "AI Provider", "Value": "Google Gemini"},
        ]
        st.dataframe(pd.DataFrame(app_data),
                     use_container_width=True, hide_index=True)

    st.markdown("#### Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("🔄 Refresh Metrics", use_container_width=True):
            st.rerun()
    with action_col2:
        if st.button("📊 Export Health Report", use_container_width=True):
            st.info("Health report export will be available in a future update.")
    with action_col3:
        if st.button("🔔 Configure Alerts", use_container_width=True):
            st.info("Alert configuration will be available in a future update.")
