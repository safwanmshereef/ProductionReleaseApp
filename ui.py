import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
            --bg-primary: #0f1419;
            --bg-secondary: #15202b;
            --bg-tertiary: #192734;
            --bg-elevated: #22303c;
            --surface: rgba(255, 255, 255, 0.04);
            --surface-hover: rgba(255, 255, 255, 0.08);
            --text-primary: #e7e9ea;
            --text-secondary: #8b98a5;
            --text-muted: #6e767d;
            --accent-blue: #1d9bf0;
            --accent-green: #00ba7c;
            --accent-yellow: #ffb800;
            --accent-orange: #ff7a00;
            --accent-red: #f4212e;
            --accent-purple: #7856ff;
            --accent-cyan: #22d3ee;
            --accent-violet: #a78bfa;
            --border: rgba(255, 255, 255, 0.08);
            --border-strong: rgba(255, 255, 255, 0.15);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
            --radius-xl: 20px;
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        .stApp {
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
        }

        .main .block-container {
            position: relative;
            z-index: 1;
        }

        .block-container {
            max-width: 1400px;
            padding: 0.85rem 2rem 2.4rem;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            letter-spacing: -0.01em;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        h1 { font-size: 1.75rem; font-weight: 800; }
        h2 { font-size: 1.375rem; }
        h3 { font-size: 1.125rem; }
        h4 { font-size: 1rem; }

        p, span, div {
            color: var(--text-secondary);
        }

        /* Hero Section - Compact & Modern */
        .hero-section {
            position: relative;
            padding: 0.62rem 0.9rem;
            border-radius: var(--radius-lg);
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            margin-bottom: 0.5rem;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.16rem 0.45rem;
            border-radius: var(--radius-sm);
            background: rgba(29, 155, 240, 0.12);
            font-size: 0.58rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            color: var(--accent-blue);
            margin-bottom: 0.22rem;
        }

        .hero-badge::before {
            content: "";
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 6px var(--accent-green);
        }

        .hero-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 1.12rem;
            line-height: 1.08;
            margin: 0 0 0.1rem 0;
            color: var(--text-primary);
        }

        .hero-subtitle {
            color: var(--text-secondary);
            font-size: 0.74rem;
            line-height: 1.2;
            max-width: 680px;
            margin: 0;
        }

        /* Metric Cards - Clean Cards */
        .metric-card {
            position: relative;
            padding: 0.58rem 0.72rem;
            border-radius: var(--radius-md);
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            transition: all 0.2s ease;
            min-height: 70px;
        }

        .metric-card:hover {
            border-color: var(--border-strong);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .metric-card.positive { border-left: 3px solid var(--accent-green); }
        .metric-card.negative { border-left: 3px solid var(--accent-red); }
        .metric-card.neutral { border-left: 3px solid var(--accent-blue); }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.68rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.2rem;
        }

        .metric-value {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1;
            color: var(--text-primary);
            margin-bottom: 0.12rem;
        }

        .metric-delta {
            font-size: 0.82rem;
            font-weight: 500;
            line-height: 1.1;
        }

        .metric-delta.positive { color: var(--accent-green); }
        .metric-delta.negative { color: var(--accent-red); }
        .metric-delta.neutral { color: var(--text-muted); }

        /* Status Chips - Refined Pills */
        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.25rem 0.6rem;
            border-radius: var(--radius-sm);
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }

        .status-chip::before {
            content: "";
            width: 5px;
            height: 5px;
            border-radius: 50%;
        }

        .status-chip.running, .status-chip.open, .status-chip.in-progress, .status-chip.active {
            color: var(--accent-blue);
            background: rgba(29, 155, 240, 0.12);
        }
        .status-chip.running::before, .status-chip.open::before, .status-chip.in-progress::before, .status-chip.active::before {
            background: var(--accent-blue);
        }

        .status-chip.completed, .status-chip.resolved, .status-chip.closed, .status-chip.healthy, .status-chip.met {
            color: var(--accent-green);
            background: rgba(0, 186, 124, 0.12);
        }
        .status-chip.completed::before, .status-chip.resolved::before, .status-chip.closed::before, .status-chip.healthy::before, .status-chip.met::before {
            background: var(--accent-green);
        }

        .status-chip.failed, .status-chip.critical, .status-chip.breached {
            color: var(--accent-red);
            background: rgba(244, 33, 46, 0.12);
        }
        .status-chip.failed::before, .status-chip.critical::before, .status-chip.breached::before {
            background: var(--accent-red);
        }

        .status-chip.queued, .status-chip.waiting-on-user, .status-chip.paused, .status-chip.at-risk, .status-chip.degraded, .status-chip.alert {
            color: var(--accent-yellow);
            background: rgba(255, 184, 0, 0.12);
        }
        .status-chip.queued::before, .status-chip.waiting-on-user::before, .status-chip.paused::before, .status-chip.at-risk::before, .status-chip.degraded::before, .status-chip.alert::before {
            background: var(--accent-yellow);
        }

        .status-chip.high {
            color: var(--accent-orange);
            background: rgba(255, 122, 0, 0.12);
        }
        .status-chip.high::before {
            background: var(--accent-orange);
        }

        .status-chip.medium {
            color: var(--accent-blue);
            background: rgba(29, 155, 240, 0.12);
        }
        .status-chip.medium::before {
            background: var(--accent-blue);
        }

        .status-chip.low, .status-chip.idle, .status-chip.on-track, .status-chip.pending {
            color: var(--text-muted);
            background: rgba(110, 118, 125, 0.15);
        }
        .status-chip.low::before, .status-chip.idle::before, .status-chip.on-track::before, .status-chip.pending::before {
            background: var(--text-muted);
        }

        /* Surface Cards */
        .surface-card {
            position: relative;
            padding: 1rem;
            border-radius: var(--radius-md);
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }

        .surface-card:hover {
            border-color: var(--border-strong);
        }

        /* Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 0.25rem;
            gap: 0.125rem;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-sm);
            padding: 0.5rem 1rem;
            font-weight: 600;
            font-size: 0.8rem;
            color: var(--text-secondary);
            background: transparent;
            border: none;
            transition: all 0.15s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary);
            background: var(--surface);
        }

        .stTabs [aria-selected="true"] {
            background: var(--bg-elevated) !important;
            color: var(--text-primary) !important;
        }

        /* DataFrames & Tables */
        .stDataFrame, .stTable {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            overflow: hidden;
        }

        [data-testid="stDataFrame"] {
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
        }

        /* Buttons */
        .stButton > button {
            border-radius: var(--radius-md);
            background: var(--accent-blue);
            color: white;
            border: none;
            font-weight: 600;
            font-size: 0.85rem;
            padding: 0.6rem 1.25rem;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            background: #1a8cd8;
            transform: translateY(-1px);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        .stButton > button:disabled {
            background: var(--bg-elevated) !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border) !important;
            opacity: 1 !important;
            cursor: not-allowed !important;
            box-shadow: none !important;
        }

        /* Form Inputs */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stNumberInput input {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            padding: 0.6rem 0.75rem !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 2px rgba(29, 155, 240, 0.2) !important;
        }

        .stTextInput > div > div > input::placeholder,
        .stTextArea textarea::placeholder {
            color: var(--text-muted) !important;
        }

        /* Selectbox & MultiSelect - Fixed Purple Issue */
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            background: var(--bg-secondary) !important;
        }

        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
        }

        .stSelectbox [data-baseweb="select"] > div:hover,
        .stMultiSelect [data-baseweb="select"] > div:hover {
            border-color: var(--border-strong) !important;
        }

        /* MultiSelect Tags - Clean Style */
        [data-baseweb="tag"] {
            background: var(--bg-elevated) !important;
            border: 1px solid var(--border-strong) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text-primary) !important;
        }

        [data-baseweb="tag"] span {
            color: var(--text-primary) !important;
        }

        [data-baseweb="tag"]:hover {
            background: var(--surface-hover) !important;
        }

        /* Dropdown Menu */
        [data-baseweb="popover"] > div,
        [data-baseweb="menu"] {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-lg) !important;
        }

        [data-baseweb="menu"] li {
            background: transparent !important;
        }

        [data-baseweb="menu"] li:hover {
            background: var(--surface) !important;
        }

        /* Alerts */
        .stAlert {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
        }

        .stSuccess { border-left: 3px solid var(--accent-green) !important; }
        .stInfo { border-left: 3px solid var(--accent-blue) !important; }
        .stWarning { border-left: 3px solid var(--accent-yellow) !important; }
        .stError { border-left: 3px solid var(--accent-red) !important; }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text-secondary);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--text-primary);
        }

        [data-testid="stSidebarNav"] a {
            color: var(--text-secondary) !important;
            padding: 0.6rem 0.75rem;
            border-radius: var(--radius-sm);
            margin: 0.125rem 0.5rem;
            transition: all 0.15s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: var(--surface);
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            background: var(--bg-elevated) !important;
            color: var(--text-primary) !important;
        }

        /* Page Links */
        .stPageLink > a {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1rem !important;
            transition: all 0.15s ease !important;
        }

        .stPageLink > a:hover {
            background: var(--bg-elevated) !important;
            border-color: var(--border-strong) !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
        }

        /* Chat */
        [data-testid="stChatMessage"] {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem !important;
        }

        [data-testid="stChatInput"] {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
        }

        /* Download Button */
        .stDownloadButton > button {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
        }

        .stDownloadButton > button:hover {
            background: var(--bg-elevated) !important;
            border-color: var(--border-strong) !important;
        }

        pre, code {
            color: #cbd5e1 !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--bg-elevated);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--border-strong);
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            overflow: hidden;
        }

        th, td {
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background: var(--bg-tertiary);
            font-weight: 600;
            color: var(--text-primary);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        tr:hover {
            background: var(--surface);
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .block-container {
                padding: 0.7rem 1rem 1.5rem;
            }

            .hero-section {
                padding: 0.56rem 0.72rem;
            }

            .hero-title {
                font-size: 1.04rem;
            }

            .hero-subtitle {
                font-size: 0.7rem;
            }
        }

        @media (max-width: 768px) {
            .metric-card {
                padding: 0.54rem 0.62rem;
                min-height: 64px;
            }

            .metric-value {
                font-size: 1.4rem;
            }

            .metric-label {
                font-size: 0.62rem;
            }

            .metric-delta {
                font-size: 0.76rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title, subtitle, chip_text="Enterprise Operations"):
    st.markdown(
        f"""
        <section class="hero-section">
            <div class="hero-badge">{chip_text}</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, delta="", tone="neutral"):
    tone_class = tone if tone in ["positive",
                                  "negative", "neutral"] else "neutral"

    st.markdown(
        f"""
        <div class="metric-card {tone_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta {tone_class}">{delta}</div>
        </div>
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
