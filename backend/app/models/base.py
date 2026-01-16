from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declared_attr
from app.db.base import Base

class TenantAwareModel(Base):
    """
    Mixin to add tenant_id to a model and enforce tenant isolation.
    Abstract base class to be inherited by tenant-specific models.
    """
    __abstract__ = True

    @declared_attr
    def tenant_id(cls):
        # In a real app, this might refer to a 'tenants' table. 
        # For now, we assume tenant_id is a string UUID.
        # We also assume 'tenants' table exists or will exist.
        return Column(String, index=True, nullable=False)
