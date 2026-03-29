import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-tertiary: #1a1a24;
            --surface: rgba(255, 255, 255, 0.03);
            --surface-hover: rgba(255, 255, 255, 0.06);
            --surface-strong: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-violet: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-pink: #ec4899;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f43f5e 100%);
            --gradient-secondary: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
            --gradient-accent: linear-gradient(135deg, #ec4899 0%, #8b5cf6 50%, #06b6d4 100%);
            --border-subtle: rgba(255, 255, 255, 0.06);
            --border-glow: rgba(139, 92, 246, 0.3);
            --shadow-glow: 0 0 60px rgba(139, 92, 246, 0.15);
            --shadow-card: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
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
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: 
                radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 20%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 40% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 70%, rgba(16, 185, 129, 0.08) 0%, transparent 35%);
            animation: aurora 20s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }

        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            background: 
                radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139, 92, 246, 0.2), transparent),
                radial-gradient(ellipse 60% 40% at 100% 50%, rgba(6, 182, 212, 0.15), transparent),
                radial-gradient(ellipse 50% 30% at 0% 80%, rgba(236, 72, 153, 0.12), transparent);
            pointer-events: none;
            z-index: 0;
        }

        @keyframes aurora {
            0%, 100% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(3deg) scale(1.02); }
            50% { transform: rotate(-2deg) scale(0.98); }
            75% { transform: rotate(1deg) scale(1.01); }
        }

        .main .block-container {
            position: relative;
            z-index: 1;
        }

        .block-container {
            max-width: 1400px;
            padding: 2rem 2rem 3rem;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        h1 { font-size: 2.5rem; font-weight: 800; }
        h2 { font-size: 1.875rem; }
        h3 { font-size: 1.5rem; }
        h4 { font-size: 1.25rem; }

        p, span, div {
            color: var(--text-secondary);
        }

        /* Hero Section */
        .hero-section {
            position: relative;
            padding: 2.5rem;
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.08) 50%, rgba(236, 72, 153, 0.06) 100%);
            border: 1px solid var(--border-subtle);
            margin-bottom: 2rem;
            overflow: hidden;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }

        .hero-section::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), rgba(6, 182, 212, 0.5), transparent);
        }

        .hero-section::after {
            content: "";
            position: absolute;
            width: 400px;
            height: 400px;
            right: -150px;
            top: -200px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.2) 0%, transparent 70%);
            pointer-events: none;
            animation: pulse-glow 4s ease-in-out infinite;
        }

        @keyframes pulse-glow {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.1); }
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.2));
            border: 1px solid rgba(139, 92, 246, 0.3);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--accent-cyan);
            margin-bottom: 1rem;
        }

        .hero-badge::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-emerald);
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }

        .hero-title {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.1;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 50%, #f8fafc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-subtitle {
            color: var(--text-secondary);
            font-size: 1.125rem;
            line-height: 1.6;
            max-width: 600px;
        }

        /* Metric Cards - Premium Glass Design */
        .metric-card {
            position: relative;
            padding: 1.5rem;
            border-radius: var(--radius-lg);
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }

        .metric-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        }

        .metric-card:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(139, 92, 246, 0.3);
            transform: translateY(-4px);
            box-shadow: 
                0 20px 40px -15px rgba(0, 0, 0, 0.5),
                0 0 30px rgba(139, 92, 246, 0.1);
        }

        .metric-card.positive { border-left: 3px solid var(--accent-emerald); }
        .metric-card.negative { border-left: 3px solid var(--accent-rose); }
        .metric-card.neutral { border-left: 3px solid var(--accent-violet); }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            font-family: 'Inter', sans-serif;
            font-size: 2.25rem;
            font-weight: 800;
            line-height: 1;
            background: var(--gradient-secondary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.25rem;
        }

        .metric-delta {
            font-size: 0.8rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .metric-delta.positive { color: var(--accent-emerald); }
        .metric-delta.negative { color: var(--accent-rose); }
        .metric-delta.neutral { color: var(--text-muted); }

        /* Status Chips - Neon Style */
        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.375rem 0.875rem;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            transition: all 0.2s ease;
        }

        .status-chip::before {
            content: "";
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }

        .status-chip.running, .status-chip.open, .status-chip.in-progress {
            color: #22d3ee;
            background: rgba(6, 182, 212, 0.15);
            border: 1px solid rgba(6, 182, 212, 0.3);
        }
        .status-chip.running::before, .status-chip.open::before, .status-chip.in-progress::before {
            background: #22d3ee;
            box-shadow: 0 0 8px #22d3ee;
            animation: pulse 1.5s ease-in-out infinite;
        }

        .status-chip.completed, .status-chip.resolved, .status-chip.closed {
            color: #34d399;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .status-chip.completed::before, .status-chip.resolved::before, .status-chip.closed::before {
            background: #34d399;
            box-shadow: 0 0 8px #34d399;
        }

        .status-chip.failed, .status-chip.critical {
            color: #fb7185;
            background: rgba(244, 63, 94, 0.15);
            border: 1px solid rgba(244, 63, 94, 0.3);
        }
        .status-chip.failed::before, .status-chip.critical::before {
            background: #fb7185;
            box-shadow: 0 0 8px #fb7185;
            animation: pulse 1s ease-in-out infinite;
        }

        .status-chip.queued, .status-chip.waiting-on-user, .status-chip.paused {
            color: #fbbf24;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .status-chip.queued::before, .status-chip.waiting-on-user::before, .status-chip.paused::before {
            background: #fbbf24;
            box-shadow: 0 0 8px #fbbf24;
        }

        .status-chip.high {
            color: #f97316;
            background: rgba(249, 115, 22, 0.15);
            border: 1px solid rgba(249, 115, 22, 0.3);
        }
        .status-chip.high::before {
            background: #f97316;
            box-shadow: 0 0 8px #f97316;
        }

        .status-chip.medium {
            color: #a78bfa;
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }
        .status-chip.medium::before {
            background: #a78bfa;
            box-shadow: 0 0 8px #a78bfa;
        }

        .status-chip.low {
            color: #94a3b8;
            background: rgba(148, 163, 184, 0.1);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .status-chip.low::before {
            background: #94a3b8;
        }

        /* Surface Cards */
        .surface-card {
            position: relative;
            padding: 1.25rem;
            border-radius: var(--radius-lg);
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .surface-card:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(139, 92, 246, 0.2);
            transform: translateY(-2px);
        }

        /* Streamlit Tabs - Modern Pills */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 0.375rem;
            gap: 0.25rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-md);
            padding: 0.625rem 1.25rem;
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--text-secondary);
            background: transparent;
            border: none;
            transition: all 0.2s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.04);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.15)) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        /* DataFrames & Tables */
        .stDataFrame, .stTable {
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.01) !important;
        }

        .stDataFrame > div, .stTable > div {
            background: transparent !important;
        }

        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.01);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }

        /* Modern Buttons */
        .stButton > button {
            position: relative;
            border-radius: var(--radius-md);
            background: linear-gradient(135deg, var(--accent-violet), var(--accent-cyan));
            color: white;
            border: none;
            font-weight: 600;
            font-size: 0.875rem;
            padding: 0.75rem 1.5rem;
            box-shadow: 
                0 4px 15px rgba(139, 92, 246, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }

        .stButton > button::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 8px 25px rgba(139, 92, 246, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }

        .stButton > button:hover::before {
            opacity: 1;
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Form Inputs - Dark Glassmorphism */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stNumberInput input {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: var(--accent-violet) !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }

        .stTextInput > div > div > input::placeholder,
        .stTextArea textarea::placeholder {
            color: var(--text-muted) !important;
        }

        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-md) !important;
        }

        .stSelectbox [data-baseweb="select"] > div:hover,
        .stMultiSelect [data-baseweb="select"] > div:hover {
            border-color: rgba(139, 92, 246, 0.3) !important;
        }

        /* Alerts */
        .stAlert {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-md) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        [data-testid="stAlert"] > div {
            color: var(--text-secondary);
        }

        /* Success Alert */
        .stSuccess {
            border-left: 3px solid var(--accent-emerald) !important;
        }

        /* Info Alert */
        .stInfo {
            border-left: 3px solid var(--accent-cyan) !important;
        }

        /* Warning Alert */
        .stWarning {
            border-left: 3px solid var(--accent-amber) !important;
        }

        /* Error Alert */
        .stError {
            border-left: 3px solid var(--accent-rose) !important;
        }

        /* Sidebar - Dark Glass */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(18, 18, 26, 0.98), rgba(10, 10, 15, 0.95)) !important;
            border-right: 1px solid var(--border-subtle);
        }

        [data-testid="stSidebar"] * {
            color: var(--text-secondary);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--text-primary);
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        [data-testid="stSidebarNav"] a {
            color: var(--text-secondary) !important;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            margin: 0.25rem 0.5rem;
            transition: all 0.2s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(139, 92, 246, 0.1);
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.1)) !important;
            color: var(--text-primary) !important;
            border-left: 2px solid var(--accent-violet);
        }

        /* Page Links */
        .stPageLink > a {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-md) !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }

        .stPageLink > a:hover {
            background: rgba(139, 92, 246, 0.1) !important;
            border-color: rgba(139, 92, 246, 0.3) !important;
            transform: translateX(4px);
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            background: rgba(255, 255, 255, 0.02);
            border-radius: var(--radius-md);
        }

        .streamlit-expanderHeader:hover {
            background: rgba(255, 255, 255, 0.04);
        }

        /* Chat Messages */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1rem !important;
        }

        [data-testid="stChatMessage"][data-testid*="user"] {
            background: rgba(139, 92, 246, 0.05) !important;
            border-color: rgba(139, 92, 246, 0.2) !important;
        }

        /* Chat Input */
        [data-testid="stChatInput"] {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-lg) !important;
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: var(--accent-violet) !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
        }

        /* Checkboxes & Toggles */
        .stCheckbox label span,
        .stToggle label span {
            color: var(--text-secondary) !important;
        }

        /* Download Button */
        .stDownloadButton > button {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--border-subtle) !important;
            color: var(--text-primary) !important;
        }

        .stDownloadButton > button:hover {
            background: rgba(139, 92, 246, 0.1) !important;
            border-color: rgba(139, 92, 246, 0.3) !important;
        }

        /* Form Submit Button */
        [data-testid="stFormSubmitButton"] > button {
            width: 100%;
        }

        /* Spinner */
        .stSpinner > div {
            border-color: var(--accent-violet) transparent transparent transparent !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(139, 92, 246, 0.3);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(139, 92, 246, 0.5);
        }

        /* Markdown Tables in HTML */
        table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.01);
            border-radius: var(--radius-md);
            overflow: hidden;
        }

        th, td {
            padding: 0.875rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-subtle);
        }

        th {
            background: rgba(255, 255, 255, 0.02);
            font-weight: 600;
            color: var(--text-primary);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        tr:hover {
            background: rgba(139, 92, 246, 0.03);
        }

        /* Responsive Design */
        @media (max-width: 1024px) {
            .block-container {
                padding: 1.5rem 1rem 2rem;
            }

            .hero-section {
                padding: 1.75rem;
            }

            .hero-title {
                font-size: 1.75rem;
            }

            .metric-value {
                font-size: 1.75rem;
            }
        }

        @media (max-width: 768px) {
            .block-container {
                padding: 1rem 0.75rem 1.5rem;
            }

            .hero-section {
                padding: 1.25rem;
                border-radius: var(--radius-lg);
            }

            .hero-title {
                font-size: 1.5rem;
            }

            .metric-card {
                padding: 1rem;
            }

            .metric-value {
                font-size: 1.5rem;
            }
        }

        /* Animation for loading states */
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }

        .loading-shimmer {
            background: linear-gradient(90deg, 
                rgba(255, 255, 255, 0.02) 25%, 
                rgba(255, 255, 255, 0.05) 50%, 
                rgba(255, 255, 255, 0.02) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
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
    tone_class = tone if tone in ["positive", "negative", "neutral"] else "neutral"

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
