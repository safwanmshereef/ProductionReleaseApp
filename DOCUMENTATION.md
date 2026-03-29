# Enterprise Ops Hub - Technical Documentation

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Core Components](#core-components)
- [Data Models](#data-models)
- [Feature Workflows](#feature-workflows)
- [AI Integration](#ai-integration)
- [API Reference](#api-reference)

---

## Overview

Enterprise Ops Hub is a production-grade operations management platform built with Streamlit. It provides a unified workspace for:

- **Pipeline Monitoring** - Track job execution, SLA compliance, and system health
- **Incident Management** - AI-assisted ticket triage and resolution workflows
- **Knowledge Base** - Context-aware AI assistant for operational guidance

### Design Philosophy

1. **Single Pane of Glass** - All operational data visible in one place
2. **AI-First** - Intelligent automation for routine tasks
3. **Action-Oriented** - Every view enables immediate action
4. **Production-Safe** - Designed for critical operations environments

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   app.py     │  │   pages/     │  │    ui.py     │           │
│  │  (Homepage)  │  │ (Sub-pages)  │  │  (Styling)   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BUSINESS LAYER                            │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │     ai_service.py    │  │       db.py          │             │
│  │  (Gemini Integration)│  │  (Data Operations)   │             │
│  └──────────────────────┘  └──────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │   SQLite Database    │  │   Streamlit Secrets  │             │
│  │ (production_app.db)  │  │    (API Keys)        │             │
│  └──────────────────────┘  └──────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                           │
│  ┌──────────────────────────────────────────────┐               │
│  │              Google Gemini API               │               │
│  │         (AI Text Generation & Triage)        │               │
│  └──────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Request Flow

1. User interacts with Streamlit UI
2. Page logic processes request
3. Database operations via SQLAlchemy ORM
4. AI operations via Gemini API (when enabled)
5. Response rendered back to UI

---

## Core Components

### 1. app.py - Main Dashboard

**Purpose:** Entry point and system overview

**Key Functions:**
- Displays aggregate metrics (jobs running, success rate, open tickets)
- Quick navigation to sub-pages
- System health snapshot with module status
- Recent activity feeds for jobs and tickets

**Data Flow:**
```python
init_db()           # Ensure database is ready
session.query(Job)  # Fetch all jobs
session.query(Ticket)  # Fetch all tickets
# Compute metrics
# Render dashboard
```

### 2. ui.py - UI Components

**Purpose:** Centralized styling and reusable components

**Components:**
| Function | Description |
|----------|-------------|
| `inject_global_styles()` | Injects CSS for dark glassmorphism theme |
| `render_header()` | Creates hero section with title and badge |
| `metric_card()` | Displays KPI metrics with visual indicators |
| `status_chip()` | Returns HTML for colored status badges |

**CSS Architecture:**
- CSS Variables for theming consistency
- Glassmorphism effects with backdrop-filter
- Responsive breakpoints at 1024px and 768px
- Animation keyframes for pulse and aurora effects

### 3. db.py - Data Layer

**Purpose:** Database models, migrations, and operations

**Models:**

```python
class Job:
    id: int (PK)
    job_id: str (unique)      # e.g., "JOB-1001"
    job_type: str             # e.g., "ETL Pipeline"
    owner: str                # Team or individual
    status: str               # Queued|Running|Completed|Failed|Paused
    priority: str             # Low|Medium|High|Critical
    duration_min: int         # Execution time
    sla_min: int              # SLA threshold
    notes: str                # Runbook details
    created_at: datetime
    started_at: datetime
    ended_at: datetime
    last_heartbeat: datetime

class Ticket:
    id: int (PK)
    ticket_no: str (unique)   # e.g., "TKT-1001"
    title: str
    description: str
    priority: str             # Low|Medium|High|Critical
    category: str             # Bug|Feature Request|Access|Other
    status: str               # Open|In Progress|Waiting on User|Resolved|Closed
    impact: str               # Low|Medium|High
    requester: str
    assignee: str
    sentiment: str            # AI-detected sentiment
    ai_summary: str           # AI-generated summary
    root_cause: str
    resolution: str
    created_at: datetime
    updated_at: datetime

class TicketActivity:
    id: int (PK)
    ticket_id: int (FK)
    actor: str                # Who made the change
    action: str               # Created|Updated|Triage|Resolved
    note: str                 # Activity details
    created_at: datetime
```

**Key Functions:**
| Function | Description |
|----------|-------------|
| `init_db()` | Creates tables and runs migrations |
| `get_session()` | Returns new database session |
| `next_ticket_number()` | Generates sequential ticket IDs |
| `add_ticket_activity()` | Logs ticket changes |
| `_migrate_schema_if_needed()` | Handles schema updates |

### 4. ai_service.py - AI Integration

**Purpose:** Google Gemini API integration for AI features

**Functions:**

```python
def is_gemini_ready() -> bool:
    """Check if Gemini is configured and available"""

def generate_text(prompt, system_instruction, model_name, temperature, max_output_tokens) -> str:
    """Generate text using Gemini model"""

def triage_ticket(title, description) -> Dict[str, str]:
    """AI-powered ticket analysis returning priority, category, impact, sentiment, summary"""

def answer_with_context(user_prompt, context_blob, history) -> str:
    """Generate contextual response for knowledge assistant"""

def fallback_triage(title, description) -> Dict[str, str]:
    """Rule-based triage when AI unavailable"""
```

**Triage Response Format:**
```json
{
  "priority": "High",
  "category": "Bug",
  "impact": "Medium",
  "sentiment": "Urgent",
  "summary": "Database connection failure affecting user authentication..."
}
```

---

## Data Models

### Entity Relationship Diagram

```
┌──────────────┐
│     Job      │
├──────────────┤
│ id (PK)      │
│ job_id       │
│ job_type     │
│ owner        │
│ status       │
│ priority     │
│ duration_min │
│ sla_min      │
│ notes        │
│ created_at   │
│ started_at   │
│ ended_at     │
│ last_heartbeat│
└──────────────┘

┌──────────────┐       ┌──────────────────┐
│    Ticket    │       │  TicketActivity  │
├──────────────┤       ├──────────────────┤
│ id (PK)      │◄──────│ ticket_id (FK)   │
│ ticket_no    │       │ id (PK)          │
│ title        │       │ actor            │
│ description  │       │ action           │
│ priority     │       │ note             │
│ category     │       │ created_at       │
│ status       │       └──────────────────┘
│ impact       │
│ requester    │
│ assignee     │
│ sentiment    │
│ ai_summary   │
│ root_cause   │
│ resolution   │
│ created_at   │
│ updated_at   │
└──────────────┘
```

### Status State Machines

**Job Status Flow:**
```
    ┌─────────┐
    │ Queued  │
    └────┬────┘
         │ start
         ▼
    ┌─────────┐     pause      ┌─────────┐
    │ Running │───────────────►│ Paused  │
    └────┬────┘◄───────────────└─────────┘
         │                        resume
         ├─────────────┐
         │ success     │ failure
         ▼             ▼
    ┌──────────┐  ┌─────────┐
    │Completed │  │ Failed  │
    └──────────┘  └─────────┘
```

**Ticket Status Flow:**
```
    ┌─────────┐
    │  Open   │
    └────┬────┘
         │ assign
         ▼
    ┌─────────────┐    needs info    ┌──────────────────┐
    │ In Progress │─────────────────►│ Waiting on User  │
    └──────┬──────┘◄─────────────────└──────────────────┘
           │                              info received
           │ fix applied
           ▼
    ┌──────────┐    verify     ┌─────────┐
    │ Resolved │──────────────►│ Closed  │
    └──────────┘               └─────────┘
```

---

## Feature Workflows

### Job Monitoring Workflow

1. **Create Job**
   ```
   User fills form → Validate input → Generate job_id → Insert to DB → Refresh UI
   ```

2. **Update Job**
   ```
   Select job → Modify fields → Update timestamps → Append to notes → Commit → Refresh
   ```

3. **SLA Monitoring**
   ```
   For each job:
     if status in [Running, Completed, Failed]:
       if duration_min > sla_min:
         mark as SLA Breach
   ```

### Ticket Triage Workflow

```
┌────────────────┐
│ User submits   │
│ ticket form    │
└───────┬────────┘
        │
        ▼
┌────────────────┐     No      ┌────────────────┐
│ AI triage      │────────────►│ Fallback rules │
│ enabled?       │             │ based triage   │
└───────┬────────┘             └───────┬────────┘
        │ Yes                          │
        ▼                              │
┌────────────────┐                     │
│ Send to Gemini │                     │
│ for analysis   │                     │
└───────┬────────┘                     │
        │                              │
        ▼                              ▼
┌────────────────────────────────────────┐
│ Extract: priority, category, impact,   │
│          sentiment, summary            │
└───────────────────┬────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│ Create ticket with triage results      │
│ Log activity: "AI Triage"              │
└────────────────────────────────────────┘
```

### Knowledge Assistant Workflow

```
┌────────────────┐
│ User asks      │
│ question       │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Build context  │◄── Include jobs? Include tickets?
│ from database  │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Append chat    │
│ history (last 8)│
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Send to Gemini │
│ with context   │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Display response│
│ Save to history │
└────────────────┘
```

---

## AI Integration

### Gemini Configuration

**Required Setup:**
1. Create `.streamlit/secrets.toml`
2. Add `GOOGLE_API_KEY = "your-key"`

**Model Used:** `gemini-1.5-flash`

**Configuration Parameters:**
| Parameter | Triage | Assistant |
|-----------|--------|-----------|
| Temperature | 0.2 | 0.35 |
| Max Tokens | 300 | 900 |
| System Instruction | JSON only | Production guidance |

### Fallback Behavior

When Gemini is unavailable, the system uses rule-based logic:

```python
# Priority Detection
"down", "outage", "critical", "p1", "urgent" → Critical
"error", "fail", "broken", "issue" → High

# Category Detection  
"access", "permission", "role", "login" → Access
"feature", "enhancement", "improve" → Feature Request
"bug", "exception", "trace", "error" → Bug
```

---

## API Reference

### Database Functions

```python
# Initialize database (creates tables, runs migrations, seeds data)
init_db() -> None

# Get new database session (must be closed after use)
get_session() -> Session

# Generate next ticket number
next_ticket_number(session) -> str  # Returns "TKT-XXXX"

# Log ticket activity
add_ticket_activity(session, ticket_id, actor, action, note) -> None
```

### AI Functions

```python
# Check if Gemini is configured
is_gemini_ready() -> bool

# Generate text with Gemini
generate_text(
    prompt: str,
    system_instruction: str = "",
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.3,
    max_output_tokens: int = 800
) -> str

# Triage a ticket with AI
triage_ticket(title: str, description: str) -> Dict[str, str]
# Returns: {priority, category, impact, sentiment, summary}

# Get AI response with operational context
answer_with_context(
    user_prompt: str,
    context_blob: str,
    history: List[Dict[str, str]]
) -> str
```

### UI Functions

```python
# Inject global CSS styles
inject_global_styles() -> None

# Render hero header section
render_header(title: str, subtitle: str, chip_text: str = "Enterprise Operations") -> None

# Render metric card
metric_card(label: str, value: Any, delta: str = "", tone: str = "neutral") -> None
# tone: "positive" | "negative" | "neutral"

# Generate status chip HTML
status_chip(value: str) -> str
```

---

## Performance Considerations

1. **Database Sessions** - Always close sessions after use
2. **Query Optimization** - Use `.limit()` for large datasets
3. **Caching** - Streamlit's `@st.cache_data` can be added for expensive operations
4. **AI Calls** - Rate limited by Gemini API quotas

---

## Security Notes

1. **Secrets** - Never commit `.streamlit/secrets.toml`
2. **SQL Injection** - Protected by SQLAlchemy ORM
3. **XSS** - User input sanitized before HTML rendering
4. **API Keys** - Loaded from secure secrets management

---

## Extending the Application

### Adding a New Page

1. Create `pages/N_🔧_PageName.py`
2. Import common modules:
   ```python
   from db import get_session, init_db
   from ui import inject_global_styles, render_header
   ```
3. Call `inject_global_styles()` and `init_db()` at start
4. Use `render_header()` for consistent styling

### Adding a New Model

1. Define class in `db.py` extending `Base`
2. Add seed function `_seed_modelname()`
3. Call seed in `init_db()`
4. Add migration in `_migrate_schema_if_needed()`

### Customizing AI Behavior

1. Modify prompts in `ai_service.py`
2. Adjust `temperature` for creativity vs consistency
3. Update `fallback_triage()` rules for offline behavior

---

*Last Updated: March 2026*
