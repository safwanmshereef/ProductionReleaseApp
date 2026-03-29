import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
            --bg-primary: #0a0e14;
            --bg-secondary: #131821;
            --bg-tertiary: #1a2332;
            --bg-elevated: #212d3e;
            --surface: rgba(255, 255, 255, 0.03);
            --surface-hover: rgba(255, 255, 255, 0.06);
            --glass: rgba(255, 255, 255, 0.04);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-primary: #f1f3f5;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #3b82f6;
            --accent-blue-glow: rgba(59, 130, 246, 0.3);
            --accent-green: #10b981;
            --accent-green-glow: rgba(16, 185, 129, 0.3);
            --accent-yellow: #fbbf24;
            --accent-orange: #f97316;
            --accent-red: #ef4444;
            --accent-red-glow: rgba(239, 68, 68, 0.3);
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-violet: #a78bfa;
            --gradient-primary: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            --gradient-accent: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
            --border: rgba(255, 255, 255, 0.06);
            --border-strong: rgba(255, 255, 255, 0.12);
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.6);
            --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.15);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        .stApp {
            background: var(--bg-primary);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.06) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.04) 0px, transparent 50%);
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
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(12px);
            box-shadow: var(--shadow-md), inset 0 1px 0 rgba(255,255,255,0.05);
            margin-bottom: 0.5rem;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
            opacity: 0.3;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.16rem 0.45rem;
            border-radius: var(--radius-sm);
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
            border: 1px solid rgba(59, 130, 246, 0.2);
            font-size: 0.58rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            color: var(--accent-blue);
            margin-bottom: 0.22rem;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.1);
        }

        .hero-badge::before {
            content: "";
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 8px var(--accent-green), 0 0 4px var(--accent-green);
            animation: pulse-glow 2s ease-in-out infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(0.9); }
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
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(8px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            min-height: 70px;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: var(--gradient-primary);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .metric-card:hover {
            border-color: var(--border-strong);
            transform: translateY(-3px) scale(1.01);
            box-shadow: var(--shadow-md), var(--shadow-glow);
        }
        
        .metric-card:hover::before {
            opacity: 1;
        }

        .metric-card.positive { border-left: 2px solid var(--accent-green); box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.05); }
        .metric-card.negative { border-left: 2px solid var(--accent-red); box-shadow: inset 0 0 20px rgba(239, 68, 68, 0.05); }
        .metric-card.neutral { border-left: 2px solid var(--accent-blue); box-shadow: inset 0 0 20px rgba(59, 130, 246, 0.05); }

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
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
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
            border: 1px solid;
            transition: all 0.2s ease;
        }
        
        .status-chip:hover {
            transform: scale(1.05);
        }

        .status-chip::before {
            content: "";
            width: 5px;
            height: 5px;
            border-radius: 50%;
            animation: pulse-dot 2s ease-in-out infinite;
        }
        
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .status-chip.running, .status-chip.open, .status-chip.in-progress, .status-chip.active {
            color: var(--accent-blue);
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.3);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.1);
        }
        .status-chip.running::before, .status-chip.open::before, .status-chip.in-progress::before, .status-chip.active::before {
            background: var(--accent-blue);
            box-shadow: 0 0 6px var(--accent-blue);
        }

        .status-chip.completed, .status-chip.resolved, .status-chip.closed, .status-chip.healthy, .status-chip.met {
            color: var(--accent-green);
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.3);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
        }
        .status-chip.completed::before, .status-chip.resolved::before, .status-chip.closed::before, .status-chip.healthy::before, .status-chip.met::before {
            background: var(--accent-green);
            box-shadow: 0 0 6px var(--accent-green);
        }

        .status-chip.failed, .status-chip.critical, .status-chip.breached {
            color: var(--accent-red);
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.3);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.1);
        }
        .status-chip.failed::before, .status-chip.critical::before, .status-chip.breached::before {
            background: var(--accent-red);
            box-shadow: 0 0 6px var(--accent-red);
        }

        .status-chip.queued, .status-chip.waiting-on-user, .status-chip.paused, .status-chip.at-risk, .status-chip.degraded, .status-chip.alert {
            color: var(--accent-yellow);
            background: rgba(251, 191, 36, 0.15);
            border-color: rgba(251, 191, 36, 0.3);
            box-shadow: 0 0 10px rgba(251, 191, 36, 0.1);
        }
        .status-chip.queued::before, .status-chip.waiting-on-user::before, .status-chip.paused::before, .status-chip.at-risk::before, .status-chip.degraded::before, .status-chip.alert::before {
            background: var(--accent-yellow);
            box-shadow: 0 0 6px var(--accent-yellow);
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
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(8px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
        }

        .surface-card:hover {
            border-color: var(--border-strong);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
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
            background: var(--gradient-primary);
            color: white;
            border: none;
            font-weight: 600;
            font-size: 0.85rem;
            padding: 0.6rem 1.25rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
        }

        .stButton > button:active {
            transform: translateY(0) scale(0.98);
        }

        .stButton > button:disabled {
            background: var(--bg-elevated) !important;
            color: var(--text-muted) !important;
            border: 1px solid var(--border) !important;
            opacity: 0.5 !important;
            cursor: not-allowed !important;
            box-shadow: none !important;
            transform: none !important;
        }

        /* Form Inputs */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stNumberInput input {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            padding: 0.6rem 0.75rem !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(8px) !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15), 0 4px 12px rgba(59, 130, 246, 0.1) !important;
            transform: translateY(-1px) !important;
        }

        .stTextInput > div > div > input::placeholder,
        .stTextArea textarea::placeholder {
            color: var(--text-muted) !important;
        }

        /* Selectbox & MultiSelect - Fixed Purple Issue */
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
            backdrop-filter: blur(8px) !important;
        }

        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-md) !important;
            transition: all 0.3s ease !important;
        }

        .stSelectbox [data-baseweb="select"] > div:hover,
        .stMultiSelect [data-baseweb="select"] > div:hover {
            border-color: var(--border-strong) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }

        /* MultiSelect Tags - Clean Style */
        [data-baseweb="tag"] {
            background: var(--gradient-primary) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: var(--radius-sm) !important;
            color: white !important;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
            transition: all 0.2s ease !important;
        }

        [data-baseweb="tag"] span {
            color: white !important;
        }

        [data-baseweb="tag"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
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
            background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%) !important;
            border-right: 1px solid var(--glass-border);
            backdrop-filter: blur(12px);
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
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: var(--surface-hover);
            color: var(--text-primary) !important;
            border-color: var(--glass-border);
            transform: translateX(4px);
        }

        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            background: var(--gradient-primary) !important;
            color: white !important;
            border-color: rgba(59, 130, 246, 0.3);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        }

        /* Page Links */
        .stPageLink > a {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            backdrop-filter: blur(8px) !important;
        }

        .stPageLink > a:hover {
            background: var(--gradient-accent) !important;
            border-color: rgba(6, 182, 212, 0.3) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.15) !important;
            color: white !important;
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
        
        /* Hide Streamlit Branding */
        footer {
            visibility: hidden !important;
        }
        
        #MainMenu {
            visibility: hidden !important;
        }
        
        .viewerBadge_container__1QSob {
            display: none !important;
        }
        
        [data-testid="stBottom"] {
            display: none !important;
        }
        
        /* Hide deployment info */
        [data-testid="stStatusWidget"] {
            display: none !important;
        }
        
        [data-testid="stDeployButton"] {
            display: none !important;
        }
        
        .stDeployButton {
            display: none !important;
        }
        
        /* Hide "Created by" and "Hosted with" messages */
        div[data-testid="stNotification"] {
            display: none !important;
        }
        
        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title, subtitle, chip_text="Enterprise Operations", show_refresh=False, refresh_key="refresh"):
    """Render header with optional integrated refresh button"""
    col1, col2 = st.columns([11, 1])
    
    with col1:
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
    
    with col2:
        if show_refresh:
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("🔄", key=refresh_key, use_container_width=True, help="Refresh dashboard"):
                st.rerun()


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
