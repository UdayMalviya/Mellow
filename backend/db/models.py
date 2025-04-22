from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db.session import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    versions = relationship("DatasetVersion", back_populates="dataset", cascade="all, delete-orphan")


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    version = Column(String, nullable=False)  # e.g., v1, v2
    status = Column(String, default="raw")  # raw, cleaned, etc.
    file_path = Column(String, nullable=True)
    preprocessing_summary = Column(JSON, nullable=True)
    num_rows = Column(Integer, nullable=True)
    num_columns = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # dataset = relationship("Dataset", back_populates="versions")

    # Relationships
    dataset = relationship("Dataset", back_populates="versions")