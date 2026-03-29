import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700&display=swap');

        :root {
            --bg-start: #fff6e8;
            --bg-mid: #ecfcff;
            --bg-end: #eefee9;
            --surface: rgba(255, 255, 255, 0.52);
            --surface-strong: rgba(255, 255, 255, 0.74);
            --text-main: #102238;
            --text-muted: #3f5b71;
            --brand: #ff5f2e;
            --brand-secondary: #00a8cc;
            --accent: #18a06d;
            --border: rgba(255, 255, 255, 0.45);
            --shadow: 0 24px 44px rgba(8, 30, 47, 0.18);
            --card-glow: 0 0 0 1px rgba(255, 255, 255, 0.56), 0 20px 38px rgba(3, 27, 45, 0.16);
        }

        .stApp {
            background:
                radial-gradient(980px 460px at 102% -8%, rgba(0, 168, 204, 0.26), transparent 54%),
                radial-gradient(920px 420px at -4% 8%, rgba(255, 95, 46, 0.22), transparent 52%),
                radial-gradient(700px 300px at 40% 106%, rgba(24, 160, 109, 0.20), transparent 58%),
                linear-gradient(140deg, var(--bg-start), var(--bg-mid) 45%, var(--bg-end));
            color: var(--text-main);
            font-family: 'Manrope', sans-serif;
            min-height: 100vh;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: -15% -8% auto -8%;
            height: 60vh;
            background:
                radial-gradient(closest-side, rgba(255, 130, 84, 0.30), transparent),
                radial-gradient(closest-side, rgba(66, 201, 255, 0.28), transparent),
                radial-gradient(closest-side, rgba(116, 246, 160, 0.24), transparent);
            filter: blur(28px) saturate(120%);
            animation: glass-float 16s ease-in-out infinite alternate;
            pointer-events: none;
            z-index: 0;
        }

        .main .block-container {
            position: relative;
            z-index: 1;
        }

        .block-container {
            max-width: 1260px;
            padding-top: 1rem;
            padding-bottom: 2.4rem;
        }

        h1, h2, h3 {
            font-family: 'Sora', sans-serif;
            letter-spacing: -0.02em;
            color: #08233e;
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 1.28rem 1.38rem;
            border-radius: 20px;
            background: linear-gradient(132deg, rgba(255, 255, 255, 0.58), rgba(255, 255, 255, 0.34));
            border: 1px solid rgba(255, 255, 255, 0.62);
            box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.6);
            margin-bottom: 1rem;
            backdrop-filter: blur(13px) saturate(140%);
            -webkit-backdrop-filter: blur(13px) saturate(140%);
        }

        .hero-card::after {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            right: -85px;
            top: -110px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 113, 66, 0.35) 0%, rgba(255, 113, 66, 0.0) 70%);
            pointer-events: none;
        }

        .hero-title {
            font-family: 'Sora', sans-serif;
            font-weight: 800;
            font-size: clamp(1.36rem, 2.1vw, 2.1rem);
            margin-bottom: 0.2rem;
            color: #0b2a46;
        }

        .hero-subtitle {
            color: var(--text-muted);
            font-size: 0.96rem;
            margin-bottom: 0.4rem;
        }

        .chip {
            display: inline-block;
            margin-top: 0.2rem;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: linear-gradient(120deg, rgba(255, 95, 46, 0.20), rgba(0, 168, 204, 0.20));
            border: 1px solid rgba(255, 255, 255, 0.7);
            color: #0c4058;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .surface-card {
            padding: 0.95rem 1rem;
            border-radius: 18px;
            background: var(--surface);
            border: 1px solid var(--border);
            box-shadow: var(--card-glow);
            backdrop-filter: blur(12px) saturate(145%);
            -webkit-backdrop-filter: blur(12px) saturate(145%);
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }

        .surface-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.72), 0 24px 40px rgba(4, 31, 50, 0.20);
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.82rem;
            margin-bottom: 0.15rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
        }

        .metric-value {
            color: var(--text-main);
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1.1;
            font-family: 'Sora', sans-serif;
        }

        .metric-delta-positive {
            color: #047857;
            font-size: 0.86rem;
            font-weight: 600;
        }

        .metric-delta-negative {
            color: #b42318;
            font-size: 0.86rem;
            font-weight: 600;
        }

        .metric-delta-neutral {
            color: #4b5563;
            font-size: 0.86rem;
            font-weight: 600;
        }

        .status-chip {
            display: inline-block;
            padding: 0.25rem 0.58rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            border: 1px solid transparent;
            margin-right: 0.2rem;
        }

        .status-chip.running, .status-chip.open, .status-chip.in-progress {
            color: #075985;
            background: rgba(14, 165, 233, 0.19);
            border-color: rgba(255, 255, 255, 0.55);
        }

        .status-chip.completed, .status-chip.resolved, .status-chip.closed {
            color: #065f46;
            background: rgba(16, 185, 129, 0.18);
            border-color: rgba(255, 255, 255, 0.58);
        }

        .status-chip.failed, .status-chip.critical {
            color: #9f1239;
            background: rgba(244, 63, 94, 0.21);
            border-color: rgba(255, 255, 255, 0.58);
        }

        .status-chip.queued, .status-chip.waiting-on-user, .status-chip.paused {
            color: #7c2d12;
            background: rgba(249, 115, 22, 0.2);
            border-color: rgba(255, 255, 255, 0.58);
        }

        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.48);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 12px;
            padding: 0.2rem;
            gap: 0.3rem;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 0.5rem 0.9rem;
            font-weight: 700;
            color: #324152;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(120deg, rgba(255, 95, 46, 0.24), rgba(0, 168, 204, 0.22));
            border: 1px solid rgba(255, 255, 255, 0.62);
            color: #112e45;
        }

        .stDataFrame, .stTable, [data-testid="stMetric"] {
            border: 1px solid rgba(255, 255, 255, 0.46);
            border-radius: 14px;
            overflow: hidden;
            background: var(--surface-strong);
            backdrop-filter: blur(10px) saturate(135%);
            -webkit-backdrop-filter: blur(10px) saturate(135%);
        }

        .streamlit-expanderHeader {
            font-weight: 800;
            color: #223a53;
        }

        .stButton > button {
            border-radius: 12px;
            background: linear-gradient(120deg, var(--brand), var(--brand-secondary));
            color: #ffffff;
            border: none;
            font-weight: 700;
            box-shadow: 0 12px 24px rgba(9, 36, 58, 0.25);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 28px rgba(9, 36, 58, 0.28);
            filter: saturate(110%);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.62) !important;
            border: 1px solid rgba(255, 255, 255, 0.64) !important;
            border-radius: 12px !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.42);
        }

        .stAlert {
            background: rgba(255, 255, 255, 0.56);
            border: 1px solid rgba(255, 255, 255, 0.68);
            border-radius: 14px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.66), rgba(242, 255, 252, 0.58));
            border-right: 1px solid rgba(255, 255, 255, 0.58);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        [data-testid="stSidebar"] * {
            color: #19344d;
        }

        @keyframes glass-float {
            0% {
                transform: translate3d(-2%, 0, 0) scale(1);
            }
            50% {
                transform: translate3d(1%, 3%, 0) scale(1.04);
            }
            100% {
                transform: translate3d(2%, -1%, 0) scale(1.01);
            }
        }

        @media (max-width: 900px) {
            .block-container {
                padding-top: 0.8rem;
            }

            .hero-card {
                padding: 0.95rem;
                border-radius: 14px;
            }

            .metric-value {
                font-size: 1.35rem;
            }

            .stApp::before {
                height: 50vh;
                filter: blur(22px);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title, subtitle, chip_text="Enterprise Operations"):
    st.markdown(
        f"""
        <section class="hero-card">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <span class="chip">{chip_text}</span>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, delta="", tone="neutral"):
    tone_class = {
        "positive": "metric-delta-positive",
        "negative": "metric-delta-negative",
        "neutral": "metric-delta-neutral",
    }.get(tone, "metric-delta-neutral")

    st.markdown(
        f"""
        <section class="surface-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="{tone_class}">{delta}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def status_chip(value):
    css_class = value.lower().replace(" ", "-") if value else "open"
    return (
        f"<span class='status-chip {css_class}'>{value}</span>"
        if value
        else "<span class='status-chip'>Unknown</span>"
    )
