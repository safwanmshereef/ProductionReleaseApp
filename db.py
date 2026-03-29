from datetime import datetime, timedelta
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    inspect,
    text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///production_app.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

JOB_STATUS_OPTIONS = ["Queued", "Running", "Completed", "Failed", "Paused"]
JOB_PRIORITY_OPTIONS = ["Low", "Medium", "High", "Critical"]
TICKET_STATUS_OPTIONS = ["Open", "In Progress",
                         "Waiting on User", "Resolved", "Closed"]


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    job_type = Column(String, index=True)
    owner = Column(String, nullable=True)
    status = Column(String, default="Queued", index=True)
    priority = Column(String, default="Medium")
    duration_min = Column(Integer, default=0)
    sla_min = Column(Integer, default=60)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_no = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    priority = Column(String, default="Medium")
    category = Column(String, default="Other")
    status = Column(String, default="Open", index=True)
    impact = Column(String, default="Low")
    requester = Column(String, nullable=True)
    assignee = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    ai_summary = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    activities = relationship(
        "TicketActivity",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )


class TicketActivity(Base):
    __tablename__ = "ticket_activities"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey(
        "tickets.id"), index=True, nullable=False)
    actor = Column(String, nullable=True)
    action = Column(String, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="activities")


def _ensure_column_exists(table_name, column_name, column_sql):
    inspector = inspect(engine)
    existing_columns = {col["name"]
                        for col in inspector.get_columns(table_name)}
    if column_name in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_sql}")
        )


def _migrate_schema_if_needed():
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    if "jobs" in tables:
        _ensure_column_exists("jobs", "owner", "TEXT")
        _ensure_column_exists("jobs", "priority", "TEXT")
        _ensure_column_exists("jobs", "sla_min", "INTEGER")
        _ensure_column_exists("jobs", "notes", "TEXT")
        _ensure_column_exists("jobs", "started_at", "DATETIME")
        _ensure_column_exists("jobs", "ended_at", "DATETIME")
        _ensure_column_exists("jobs", "last_heartbeat", "DATETIME")

    if "tickets" in tables:
        _ensure_column_exists("tickets", "ticket_no", "TEXT")
        _ensure_column_exists("tickets", "impact", "TEXT")
        _ensure_column_exists("tickets", "requester", "TEXT")
        _ensure_column_exists("tickets", "assignee", "TEXT")
        _ensure_column_exists("tickets", "sentiment", "TEXT")
        _ensure_column_exists("tickets", "ai_summary", "TEXT")
        _ensure_column_exists("tickets", "root_cause", "TEXT")
        _ensure_column_exists("tickets", "resolution", "TEXT")
        _ensure_column_exists("tickets", "updated_at", "DATETIME")

        with engine.begin() as connection:
            connection.execute(
                text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS idx_tickets_ticket_no "
                    "ON tickets(ticket_no)"
                )
            )


def _max_ticket_number(session):
    max_num = 1000
    tickets = session.query(Ticket.ticket_no).filter(
        Ticket.ticket_no.isnot(None)).all()
    for (ticket_no,) in tickets:
        if not ticket_no:
            continue
        if ticket_no.startswith("TKT-"):
            suffix = ticket_no.replace("TKT-", "", 1)
            if suffix.isdigit():
                max_num = max(max_num, int(suffix))
    return max_num


def next_ticket_number(session):
    return f"TKT-{_max_ticket_number(session) + 1}"


def add_ticket_activity(session, ticket_id, actor, action, note=""):
    session.add(
        TicketActivity(
            ticket_id=ticket_id,
            actor=actor or "System",
            action=action,
            note=note,
            created_at=datetime.utcnow(),
        )
    )


def _seed_jobs(session):
    if session.query(Job).count() > 0:
        return

    now = datetime.utcnow()
    jobs = [
        Job(
            job_id="JOB-1001",
            job_type="ETL Pipeline",
            owner="DataOps",
            status="Running",
            priority="High",
            duration_min=22,
            sla_min=30,
            created_at=now - timedelta(minutes=30),
            started_at=now - timedelta(minutes=22),
            last_heartbeat=now - timedelta(minutes=1),
            notes="Daily customer usage ingestion",
        ),
        Job(
            job_id="JOB-1002",
            job_type="Backup",
            owner="Infra",
            status="Completed",
            priority="Medium",
            duration_min=95,
            sla_min=120,
            created_at=now - timedelta(hours=2),
            started_at=now - timedelta(hours=2),
            ended_at=now - timedelta(minutes=20),
            last_heartbeat=now - timedelta(minutes=20),
            notes="Full snapshot backup",
        ),
        Job(
            job_id="JOB-1003",
            job_type="Model Training",
            owner="ML Platform",
            status="Failed",
            priority="Critical",
            duration_min=48,
            sla_min=45,
            created_at=now - timedelta(hours=4),
            started_at=now - timedelta(hours=4),
            ended_at=now - timedelta(hours=3, minutes=12),
            last_heartbeat=now - timedelta(hours=3, minutes=12),
            notes="GPU memory limit reached",
        ),
        Job(
            job_id="JOB-1004",
            job_type="Data Sync",
            owner="Integrations",
            status="Queued",
            priority="Low",
            duration_min=0,
            sla_min=20,
            created_at=now - timedelta(minutes=10),
            notes="Waiting for upstream lock release",
        ),
        Job(
            job_id="JOB-1005",
            job_type="Report Generation",
            owner="BI Team",
            status="Running",
            priority="Medium",
            duration_min=9,
            sla_min=25,
            created_at=now - timedelta(minutes=12),
            started_at=now - timedelta(minutes=9),
            last_heartbeat=now - timedelta(seconds=45),
            notes="Quarterly executive KPI export",
        ),
    ]
    session.add_all(jobs)


def _seed_tickets(session):
    if session.query(Ticket).count() > 0:
        tickets_without_number = (
            session.query(Ticket).filter(
                (Ticket.ticket_no.is_(None)) | (Ticket.ticket_no == "")).all()
        )
        next_num = _max_ticket_number(session)
        for ticket in tickets_without_number:
            next_num += 1
            ticket.ticket_no = f"TKT-{next_num}"
            ticket.updated_at = datetime.utcnow()
        return

    tickets = [
        Ticket(
            ticket_no="TKT-1001",
            title="Nightly ETL failed after dependency update",
            description="The ETL workflow failed on step 3 due to a schema mismatch.",
            priority="High",
            category="Bug",
            status="In Progress",
            impact="High",
            requester="ops@company.com",
            assignee="Ravi",
            sentiment="Urgent",
            ai_summary="Likely caused by uncoordinated schema migration.",
            created_at=datetime.utcnow() - timedelta(hours=5),
            updated_at=datetime.utcnow() - timedelta(hours=1),
        ),
        Ticket(
            ticket_no="TKT-1002",
            title="Request access to production dashboard",
            description="Need read-only access for on-call shift coverage.",
            priority="Low",
            category="Access",
            status="Open",
            impact="Low",
            requester="ana@company.com",
            assignee="Service Desk",
            sentiment="Neutral",
            created_at=datetime.utcnow() - timedelta(hours=2),
            updated_at=datetime.utcnow() - timedelta(hours=2),
        ),
    ]
    session.add_all(tickets)
    session.flush()

    add_ticket_activity(
        session,
        tickets[0].id,
        "System",
        "Created",
        "Ticket auto-created from failed job alert",
    )
    add_ticket_activity(
        session,
        tickets[0].id,
        "Ravi",
        "Investigation",
        "Comparing source and destination schemas",
    )
    add_ticket_activity(
        session,
        tickets[1].id,
        "System",
        "Created",
        "Submitted through self-service portal",
    )


def init_db():
    Base.metadata.create_all(bind=engine)
    _migrate_schema_if_needed()
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        _seed_jobs(session)
        _seed_tickets(session)
        session.commit()
    finally:
        session.close()


def get_session():
    return SessionLocal()
