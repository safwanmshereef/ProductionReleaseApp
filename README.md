<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini"/>
</p>

<h1 align="center">🚀 Enterprise Ops Hub</h1>

<p align="center">
  <strong>A modern, AI-powered operations dashboard for monitoring pipelines, managing incidents, and collaborating with intelligent assistants.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#installation">Installation</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#architecture">Architecture</a>
</p>

---

## ✨ Features

### 📊 Job Monitoring Dashboard
- **Real-time job tracking** with status visualization
- **SLA monitoring** with breach detection and alerts
- **Interactive charts** showing job distribution and duration trends
- **Advanced filtering** by status, priority, owner, and search
- **Job lifecycle management** - create, update, and simulate job execution
- **CSV export** for offline analysis and reporting

### 🎟️ Smart Ticketing System
- **AI-powered ticket triage** using Google Gemini for automatic categorization
- **Visual workflow board** with drag-and-drop style organization
- **Ticket workbench** for detailed incident management
- **Activity timeline** tracking all ticket changes
- **Priority and impact assessment** with intelligent suggestions
- **Analytics dashboard** with ticket volume and priority metrics

### 🧠 Knowledge Assistant
- **Context-aware AI chatbot** powered by Google Gemini
- **Operational context injection** - includes live job and ticket data
- **Quick action buttons** for common queries
- **Conversation history** with export functionality
- **Customizable response style** - concise or detailed mode
- **Playbook generation** for incident response

### 🎨 Modern UI/UX
- **Dark glassmorphism design** with vibrant gradient accents
- **Smooth animations** and micro-interactions
- **Fully responsive** layout for desktop and mobile
- **Neon-style status indicators** with pulse animations
- **Premium typography** using Inter font family
- **Accessible color contrast** for readability

---

## 🖼️ Screenshots

<details>
<summary>Click to view screenshots</summary>

### Home Dashboard
The main dashboard displays key metrics, quick navigation, and system health at a glance.

### Job Monitoring
Track all jobs with real-time status updates, SLA tracking, and interactive visualizations.

### Smart Ticketing
AI-assisted ticket management with workflow boards and detailed analytics.

### Knowledge Assistant
Chat with an AI assistant that understands your operational context.

</details>

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/safwanmshereef/ProductionReleaseApp.git
   cd ProductionReleaseApp
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:8501`

---

## ⚙️ Configuration

### Google Gemini API (Optional)

To enable AI-powered features (ticket triage, knowledge assistant), configure your Google API key:

1. **Get an API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Create secrets file**
   ```bash
   cp .streamlit/secrets.example.toml .streamlit/secrets.toml
   ```

3. **Add your API key**
   ```toml
   GOOGLE_API_KEY = "your-api-key-here"
   ```

> **Note:** The app works without Gemini configuration - AI features will use fallback logic.

### Theme Customization

Modify `.streamlit/config.toml` to customize the app theme:

```toml
[theme]
primaryColor = "#8b5cf6"      # Violet accent
backgroundColor = "#0a0a0f"    # Dark background
secondaryBackgroundColor = "#12121a"
textColor = "#f8fafc"
```

---

## 📖 Usage

### Job Monitoring

1. **View Jobs** - The overview tab shows all jobs with status distribution charts
2. **Create Jobs** - Use the Manage Jobs tab to create new job entries
3. **Update Status** - Select a job and update its status, duration, or notes
4. **Simulate Execution** - Use the simulation button to advance running jobs

### Smart Ticketing

1. **Create Tickets** - Fill out the intake form with AI triage enabled
2. **View Board** - See tickets organized by workflow status
3. **Manage Tickets** - Use the workbench for detailed ticket updates
4. **Analyze Trends** - Check analytics for ticket volume insights

### Knowledge Assistant

1. **Toggle Context** - Enable job/ticket context for relevant answers
2. **Ask Questions** - Type questions about incidents or procedures
3. **Use Quick Actions** - Click preset buttons for common queries
4. **Export Conversations** - Download chat transcripts for documentation

---

## 🏗️ Architecture

```
ProductionReleaseApp/
├── app.py                 # Main entry point & home dashboard
├── ui.py                  # UI components & global styles
├── db.py                  # Database models & operations
├── ai_service.py          # Google Gemini AI integration
├── requirements.txt       # Python dependencies
├── production_app.db      # SQLite database (auto-generated)
├── .streamlit/
│   ├── config.toml        # Streamlit theme configuration
│   └── secrets.toml       # API keys (not committed)
└── pages/
    ├── 1_📊_Job_Monitoring.py
    ├── 2_🎟️_Smart_Ticketing.py
    └── 3_🧠_Knowledge_Assistant.py
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Styling | Custom CSS (Glassmorphism) |
| Database | SQLite + SQLAlchemy |
| Charts | Plotly Express |
| AI | Google Gemini 1.5 Flash |
| Data | Pandas |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI capabilities
- [Plotly](https://plotly.com/) for interactive visualizations
- [Inter Font](https://rsms.me/inter/) for beautiful typography

---

<p align="center">
  Made with ❤️ for modern operations teams
</p>
