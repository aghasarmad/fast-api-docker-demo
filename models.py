from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base, engine


class TeaDB(Base):
    __tablename__ = "teas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    origin = Column(String, nullable=True)

# This creates tables in the DB if they don’t exist
Base.metadata.create_all(bind=engine)