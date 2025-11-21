from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from config import DB_PATH
from utils import get_logger

logger = get_logger()

Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
Session = sessionmaker(bind=engine)

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    encodings = relationship("Encoding", back_populates="person", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="person", cascade="all, delete-orphan")

class Encoding(Base):
    __tablename__ = 'encodings'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    encoding_vector = Column(LargeBinary, nullable=False)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    person = relationship("Person", back_populates="encodings")

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    check_in_time = Column(DateTime, default=datetime.now)
    check_out_time = Column(DateTime, nullable=True)
    confidence_score = Column(Float)
    session_duration = Column(Float, default=0.0) # In minutes
    
    person = relationship("Person", back_populates="attendances")

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(engine)
    logger.info("Database initialized.")

def get_session():
    return Session()

def add_person(name, email=None):
    session = get_session()
    try:
        person = Person(name=name, email=email)
        session.add(person)
        session.commit()
        logger.info(f"Added person: {name}")
        return person.id
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding person: {e}")
        return None
    finally:
        session.close()

def add_encoding(person_id, encoding_bytes, image_path=None):
    session = get_session()
    try:
        enc = Encoding(person_id=person_id, encoding_vector=encoding_bytes, image_path=image_path)
        session.add(enc)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding encoding: {e}")
    finally:
        session.close()

def get_all_encodings():
    session = get_session()
    try:
        encodings = session.query(Encoding).all()
        data = []
        for enc in encodings:
            data.append({
                "person_id": enc.person_id,
                "encoding": enc.encoding_vector
            })
        return data
    finally:
        session.close()

def mark_attendance(person_id, confidence):
    session = get_session()
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        # Check if already checked in today
        attendance = session.query(Attendance).filter_by(person_id=person_id, date=date_str).first()
        
        if attendance:
            # Update check-out time
            attendance.check_out_time = now
            duration = (now - attendance.check_in_time).total_seconds() / 60.0
            attendance.session_duration = duration
            logger.info(f"Updated attendance (Check-out) for person_id: {person_id}")
        else:
            # Create new check-in
            attendance = Attendance(
                person_id=person_id,
                date=date_str,
                check_in_time=now,
                confidence_score=confidence
            )
            session.add(attendance)
            logger.info(f"Marked attendance (Check-in) for person_id: {person_id}")
            
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error marking attendance: {e}")
        return False
    finally:
        session.close()

def get_monthly_attendance_count(person_id, month_str):
    """
    Count days present for a user in a specific month.
    month_str format: 'YYYY-MM'
    """
    session = get_session()
    try:
        # Filter by person_id and date starting with 'YYYY-MM'
        count = session.query(Attendance).filter(
            Attendance.person_id == person_id,
            Attendance.date.like(f"{month_str}%")
        ).count()
        return count
    except Exception as e:
        logger.error(f"Error counting monthly attendance: {e}")
        return 0
    finally:
        session.close()
