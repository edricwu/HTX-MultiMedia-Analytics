from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary
from datetime import datetime
from .database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    summary = Column(Text)       # detected objects + timestamps (as JSON string)
    embedding = Column(LargeBinary)  # vector stored as BLOB
    created_at = Column(DateTime, default=datetime.utcnow)


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    transcription = Column(Text)     # full transcription JSON
    embedding = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)
