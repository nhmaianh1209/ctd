import uuid
from datetime import datetime, date
from sqlalchemy import Column, Text, Float, ARRAY, TIMESTAMP, String
from sqlalchemy.dialects.postgresql import UUID, DATE
from database import Base


class Course(Base):
    __tablename__ = "courses"

    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_code       = Column(Text)
    course_name       = Column(Text, nullable=False)
    course_short_name = Column(Text)
    category          = Column(Text)
    formats           = Column(ARRAY(Text))
    dates             = Column(ARRAY(Text))   # store as TEXT 'YYYY-MM-DD', avoid timezone issues
    months            = Column(ARRAY(Text))   # ['2026-07']
    duration_hours    = Column(Float)
    audience_type     = Column(Text)
    audience_detail   = Column(Text)
    instructor_type   = Column(Text)
    instructor_detail = Column(Text)
    pic               = Column(Text)
    registration_type = Column(Text)
    registration_link = Column(Text)
    registration_other= Column(Text)
    requirements      = Column(Text)
    visibility        = Column(Text, default="public")
    created_by        = Column(Text)
    updated_by        = Column(Text)
    created_at        = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at        = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
