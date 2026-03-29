from datetime import datetime

import streamlit as st

from ai_service import answer_with_context, get_google_api_key, is_gemini_ready
from db import Job, Ticket, get_session, init_db
from ui import inject_global_styles, render_header

st.set_page_config(
    page_title="Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
)

inject_global_styles()
init_db()
render_header(
    "Knowledge Assistant",
    "Ask about incidents, jobs, and operational playbooks with context-aware AI support.",
    "Gemini Copilot",
)


def _build_context(include_jobs: bool, include_tickets: bool, limit: int = 10) -> str:
    session = get_session()
    lines = []
    try:
        if include_jobs:
            jobs = session.query(Job).order_by(
                Job.created_at.desc()).limit(limit).all()
            lines.append("Recent Jobs:")
            for item in jobs:
                lines.append(
                    " - "
                    + f"{item.job_id} | {item.job_type} | status={item.status} | "
                    + f"priority={item.priority} | duration={item.duration_min} | sla={item.sla_min}"
                )

        if include_tickets:
            tickets = session.query(Ticket).order_by(
                Ticket.created_at.desc()).limit(limit).all()
            lines.append("Recent Tickets:")
            for item in tickets:
                lines.append(
                    " - "
                    + f"{item.ticket_no or item.id} | {item.title} | status={item.status} | "
                    + f"priority={item.priority} | assignee={item.assignee or 'Unassigned'}"
                )
    finally:
        session.close()

    return "\n".join(lines) if lines else "No operational context selected."


def _init_chat_state():
    if "assistant_messages" not in st.session_state:
        st.session_state.assistant_messages = [
            {
                "role": "assistant",
                "content": "Hello, I can help with troubleshooting, runbook steps, and incident planning.",
            }
        ]


_init_chat_state()

ready = is_gemini_ready()
key_available = bool(get_google_api_key())

status_col1, status_col2, status_col3 = st.columns([1.2, 1, 1])
with status_col1:
    include_jobs = st.toggle("Include Job Context", value=True)
with status_col2:
    include_tickets = st.toggle("Include Ticket Context", value=True)
with status_col3:
    concise_mode = st.toggle("Concise Answers", value=True)

if ready:
    st.success("Gemini connection is active.")
elif key_available:
    st.warning("Google API key is set but Gemini client dependency is missing.")
else:
    st.warning(
        "Google API key is missing. Add GOOGLE_API_KEY in Streamlit secrets.")

quick_col1, quick_col2, quick_col3 = st.columns(3)
quick_prompt = ""
with quick_col1:
    if st.button("Summarize Current Risks", use_container_width=True):
        quick_prompt = "Summarize the top operational risks from current jobs and tickets."
with quick_col2:
    if st.button("Build Incident Plan", use_container_width=True):
        quick_prompt = "Create a mitigation plan for high-priority open incidents."
with quick_col3:
    if st.button("Daily Ops Brief", use_container_width=True):
        quick_prompt = "Generate a concise daily operations briefing for on-call handoff."

for message in st.session_state.assistant_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask about incidents, jobs, or procedures")
if quick_prompt:
    user_prompt = quick_prompt

if user_prompt:
    st.session_state.assistant_messages.append(
        {"role": "user", "content": user_prompt})
    st.chat_message("user").markdown(user_prompt)

    context_blob = _build_context(
        include_jobs=include_jobs, include_tickets=include_tickets)
    depth_hint = "Give a short answer with clear bullets." if concise_mode else "Provide a detailed response with reasoning and a phased action plan."
    prompt = f"{user_prompt}\n\nResponse style: {depth_hint}"

    with st.chat_message("assistant"):
        with st.spinner("Thinking through operational context..."):
            try:
                response = answer_with_context(
                    user_prompt=prompt,
                    context_blob=context_blob,
                    history=st.session_state.assistant_messages,
                )
            except Exception as exc:
                response = f"Unable to generate a response right now. Details: {exc}"
            st.markdown(response)

    st.session_state.assistant_messages.append(
        {"role": "assistant", "content": response})

st.markdown("### Conversation Controls")
control_col1, control_col2 = st.columns([1, 1])
with control_col1:
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.assistant_messages = [
            {
                "role": "assistant",
                "content": "Conversation cleared. What would you like to investigate next?",
            }
        ]
        st.rerun()

with control_col2:
    transcript = []
    for item in st.session_state.assistant_messages:
        transcript.append(f"{item['role'].upper()}: {item['content']}")
    transcript.append(
        f"\nGenerated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    st.download_button(
        label="Download Transcript",
        data="\n\n".join(transcript).encode("utf-8"),
        file_name="knowledge_assistant_transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )

with st.expander("Preview Assistant Context"):
    st.text(_build_context(include_jobs=include_jobs,
            include_tickets=include_tickets, limit=8))
