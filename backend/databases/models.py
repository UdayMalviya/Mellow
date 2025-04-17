# sqlalchemy_schema.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from backend.databases.base import Base
import datetime


# User table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    roles = relationship("Role", secondary="user_role", back_populates="users")
    logs = relationship("Log", back_populates="user")

    # Indexes
    Index('ix_users_username', username)
    Index('ix_users_email', email)


# Role table
class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    permissions = relationship("Permission", secondary="role_permissions")
    users = relationship("User", secondary="user_role", back_populates="roles")

    # Indexes
    Index('ix_roles_role_name', role_name)


# Permission table
class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Indexes
    Index('ix_permissions_permission_name', permission_name)


# Relationship between roles and permissions
class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.permission_id'), primary_key=True)

    # Foreign Key Constraints
    Index('ix_role_permission_role_id', role_id)
    Index('ix_role_permission_permission_id', permission_id)


# Relationship between users and roles
class UserRole(Base):
    __tablename__ = 'user_role'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True)

    # Foreign Key Constraints
    Index('ix_user_role_user_id', user_id)
    Index('ix_user_role_role_id', role_id)


# Tenant table
class Tenant(Base):
    __tablename__ = 'tenants'

    tenant_id = Column(Integer, primary_key=True)
    tenant_name = Column(String(100), unique=True, nullable=False)
    configuration = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    users = relationship("User", secondary="tenant_user")
    data_sources = relationship("DataSource", back_populates="tenant")
    secrets = relationship("EncryptedSecret", back_populates="tenant")
    datasets = relationship("Dataset", back_populates="tenant")  # <- MISSING?


    # Indexes
    Index('ix_tenants_tenant_name', tenant_name)


# Relationship between tenants and users
class TenantUser(Base):
    __tablename__ = 'tenant_user'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    # Foreign Key Constraints
    Index('ix_tenant_user_tenant_id', tenant_id)
    Index('ix_tenant_user_user_id', user_id)


# DataSource table
class DataSource(Base):
    __tablename__ = 'data_sources'

    source_id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'))
    source_name = Column(String(100), unique=True, nullable=False)
    source_type = Column(String(50), nullable=False)
    configuration = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    tenant = relationship("Tenant", back_populates="data_sources")
    time_series_metadata = relationship("TimeSeriesMetadata", back_populates="data_source")

    # Foreign Key Constraints
    Index('ix_data_sources_tenant_id', tenant_id)
    Index('ix_data_sources_source_name', source_name)


# TimeSeriesMetadata table
class TimeSeriesMetadata(Base):
    __tablename__ = 'time_series_metadata'

    timeseries_id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('data_sources.source_id'))
    timeseries_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    data_source = relationship("DataSource", back_populates="time_series_metadata")

    # Foreign Key Constraints
    Index('ix_time_series_metadata_source_id', source_id)


# Dataset table
class Dataset(Base):
    __tablename__ = 'datasets'

    dataset_id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'))
    dataset_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    source_id = Column(Integer, ForeignKey('data_sources.source_id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    tenant = relationship("Tenant", back_populates="datasets")
    data_source = relationship("DataSource")
    versions = relationship("DatasetVersion", back_populates="dataset")

    # Foreign Key Constraints
    Index('ix_datasets_tenant_id', tenant_id)
    Index('ix_datasets_source_id', source_id)


# DatasetVersion table
class DatasetVersion(Base):
    __tablename__ = 'dataset_versions'

    dataset_version_id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey('datasets.dataset_id'))
    version_number = Column(String(50), nullable=False)
    preprocessing_steps = Column(JSONB, nullable=True)
    storage_location = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    dataset = relationship("Dataset", back_populates="versions")

    # Foreign Key Constraints
    Index('ix_dataset_versions_dataset_id', dataset_id)


# EncryptedSecret table
class EncryptedSecret(Base):
    __tablename__ = 'encrypted_secrets'

    secret_id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'))
    secret_key = Column(String(100), nullable=False)
    secret_value = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    tenant = relationship("Tenant", back_populates="secrets")

    # Foreign Key Constraints
    Index('ix_encrypted_secrets_tenant_id', tenant_id)


# Cache table
class Cache(Base):
    __tablename__ = 'cache_table'

    cache_id = Column(Integer, primary_key=True)
    cache_key = Column(String(100), unique=True, nullable=False)
    cache_value = Column(JSONB, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Index on cache_key for faster lookup
    Index('ix_cache_table_cache_key', cache_key)


# Metric table
class Metric(Base):
    __tablename__ = 'metrics'

    metric_id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(String(100), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Index on metric_name for performance
    Index('ix_metrics_metric_name', metric_name)


# Log table
class Log(Base):
    __tablename__ = 'logs'

    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    log_level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="logs")

    # Foreign Key Constraints
    Index('ix_logs_user_id', user_id)


# ProcessTracking table
class ProcessTracking(Base):
    __tablename__ = 'process_tracking'

    process_id = Column(Integer, primary_key=True)
    process_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Index for quick searching by status and process_name
    Index('ix_process_tracking_status', status)
    Index('ix_process_tracking_process_name', process_name)

