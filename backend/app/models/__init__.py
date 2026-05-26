from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    agent_runs = relationship("AgentRun", back_populates="user", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    stored_path = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)
    page_count = Column(Integer, default=0)
    processing_status = Column(String(50), default="pending", index=True)  # pending, processing, completed, failed
    processing_error = Column(Text, nullable=True)
    processing_duration_sec = Column(Float, default=0.0)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    extractions = relationship("Extraction", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(String(36), primary_key=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    document_name = Column(String(255), nullable=False)
    page_number = Column(Integer, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    section_heading = Column(String(255), default="")
    content = Column(Text, nullable=False)
    source_type = Column(String(50), default="digital")  # digital, ocr, table
    content_hash = Column(String(64), nullable=False)
    embedding_model = Column(String(100), default="BAAI/bge-small-en-v1.5")
    qdrant_point_id = Column(String(64), nullable=True)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    document = relationship("Document", back_populates="chunks")

class Extraction(Base):
    __tablename__ = "extractions"

    id = Column(String(36), primary_key=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    schema_name = Column(String(100), nullable=False)
    extracted_data = Column(JSON, nullable=False)
    validation_status = Column(String(50), default="valid")  # valid, invalid, incomplete
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    document = relationship("Document", back_populates="extractions")

class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    document_a_id = Column(String(36), nullable=False)
    document_b_id = Column(String(36), nullable=False)
    document_a_name = Column(String(255), nullable=False)
    document_b_name = Column(String(255), nullable=False)
    comparison_category = Column(String(100), nullable=False)
    diff_results = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    goal = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    steps_trace = Column(JSON, default=list)
    final_output = Column(Text, nullable=True)
    duration_sec = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="agent_runs")

class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    report_type = Column(String(100), default="analysis")
    content_markdown = Column(Text, nullable=False)
    evidence_citations = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
