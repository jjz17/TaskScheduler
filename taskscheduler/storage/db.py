from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    DATETIME,
    text,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import ARRAY
from sqlalchemy.exc import SQLAlchemyError
import datetime

# Database Configuration
DATABASE_URL = "postgresql://jasonzhang:password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))

    workers = relationship("Worker", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    assignments = relationship("Assignment", back_populates="project")
    worker_availability = relationship("WorkerAvailability", back_populates="project")


class Worker(Base):
    __tablename__ = "workers"

    worker_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    skills = Column(ARRAY(Text), nullable=True)  # List of skills
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))

    project = relationship("Project", back_populates="workers")
    assignments = relationship("Assignment", back_populates="worker")
    worker_availability = relationship("WorkerAvailability", back_populates="worker")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    skills_required = Column(
        ARRAY(Text), nullable=True
    )  # For storing an array of skills
    duration = Column(Integer, nullable=False)  # Duration in hours
    deadline = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))

    project = relationship("Project", back_populates="tasks")
    assignments = relationship("Assignment", back_populates="task")


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False
    )
    worker_id = Column(
        Integer, ForeignKey("workers.worker_id", ondelete="CASCADE"), nullable=False
    )
    task_id = Column(
        Integer, ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=False
    )
    assigned_at = Column(
        TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc)
    )
    status = Column(
        String(50), default="pending"
    )  # Status: pending, in-progress, completed

    project = relationship("Project", back_populates="assignments")
    worker = relationship("Worker", back_populates="assignments")
    task = relationship("Task", back_populates="assignments")


class WorkerAvailability(Base):
    __tablename__ = "worker_availability"

    availability_id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(
        Integer, ForeignKey("workers.worker_id", ondelete="CASCADE"), nullable=False
    )
    project_id = Column(
        Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False
    )
    available_from = Column(TIMESTAMP, nullable=False)
    available_to = Column(TIMESTAMP, nullable=False)

    worker = relationship("Worker", back_populates="worker_availability")
    project = relationship("Project", back_populates="worker_availability")


# Initialize Database
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to test the database connection with foreign key relationships
def test_foreign_key_relationships():
    try:
        # Get a database session using the get_db function
        with next(get_db()) as db:
            # Test the relationship between Projects, Tasks, and Workers
            query = """
                SELECT p.name AS project_name, w.name AS worker_name
                FROM projects p
                JOIN workers w ON p.project_id = w.project_id
                ORDER BY p.project_id;
            """
            result = db.execute(text(query))

            # Print results
            print("Projects, Tasks, and Workers (Foreign Key Relationships):")
            for row in result.fetchall():
                # print(f"Project: {row['project_name']}, Task: {row['task_name']}, Worker: {row['worker_name']}")
                print(row)

            # Test Worker Availability (with Project) foreign key relationship
            availability_query = """
                SELECT w.name AS worker_name, p.name AS project_name, wa.available_from, wa.available_to
                FROM worker_availability wa
                JOIN workers w ON wa.worker_id = w.worker_id
                JOIN projects p ON wa.project_id = p.project_id
                ORDER BY wa.worker_id, wa.project_id;
            """
            availability_result = db.execute(text(availability_query))

            # Print worker availability
            print("\nWorker Availability and Projects:")
            for row in availability_result.fetchall():
                print(
                    row
                    # f"Worker: {row['worker_name']}, Project: {row['project_name']}, Available From: {row['available_from']}, Available To: {row['available_to']}"
                )

    except SQLAlchemyError as e:
        print("Error while connecting to the database:", e)


# Call the function to test the foreign key relationships
test_foreign_key_relationships()
