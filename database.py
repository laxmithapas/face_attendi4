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

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False) # e.g., "LOGIN", "DELETE_USER"
    details = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

def log_audit_event(event_type, details=None):
    session = get_session()
    try:
        log = AuditLog(event_type=event_type, details=details)
        session.add(log)
        session.commit()
        logger.info(f"Audit Event: {event_type} - {details}")
    except Exception as e:
        logger.error(f"Error logging audit event: {e}")
    finally:
        session.close()

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

from security import encrypt_data, decrypt_data
import shutil

# ... (imports remain same)

# ... (classes remain same)

# ... (init_db, get_session, add_person remain same)

import io
import numpy as np

# ... (imports)

def add_encoding(person_id, encoding_bytes, image_path=None):
    session = get_session()
    try:
        # Ensure data is bytes (serialize numpy array if needed)
        if isinstance(encoding_bytes, np.ndarray):
            f = io.BytesIO()
            np.save(f, encoding_bytes)
            encoding_bytes = f.getvalue()
            
        # Encrypt the encoding before storing
        encrypted_encoding = encrypt_data(encoding_bytes)
        enc = Encoding(person_id=person_id, encoding_vector=encrypted_encoding, image_path=image_path)
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
            # Decrypt the encoding
            try:
                decrypted_encoding = decrypt_data(enc.encoding_vector)
            except Exception:
                # Fallback for legacy unencrypted data
                decrypted_encoding = enc.encoding_vector
                
            data.append({
                "person_id": enc.person_id,
                "encoding": decrypted_encoding,
                "created_at": enc.created_at
            })
        return data
    finally:
        session.close()

def mark_attendance(person_id, confidence):
    session = get_session()
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        current_hour = now.hour
        
        # Check if checked in THIS HOUR (Slot-based)
        # We process slots based on the hour of check-in
        attendance = session.query(Attendance).filter(
            Attendance.person_id == person_id,
            Attendance.date == date_str
        ).all()
        
        # Find record for current hour
        current_slot_record = None
        for record in attendance:
            if record.check_in_time.hour == current_hour:
                current_slot_record = record
                break
        
        if current_slot_record:
            # Update check-out time (Frictionless: Check-out is optional but recorded if they look at camera again)
            # Only update if at least 1 minute passed to avoid instant flickers
            if (now - current_slot_record.check_in_time).total_seconds() > 60:
                current_slot_record.check_out_time = now
                duration = (now - current_slot_record.check_in_time).total_seconds() / 60.0
                current_slot_record.session_duration = duration
                logger.info(f"Updated attendance (Check-out) for person_id: {person_id} at {now}")
        else:
            # Create new check-in for this slot
            attendance = Attendance(
                person_id=person_id,
                date=date_str,
                check_in_time=now,
                check_out_time=now, # Initialize with same time (0 duration until updated)
                confidence_score=confidence,
                session_duration=0.0
            )
            session.add(attendance)
            logger.info(f"Marked attendance (Check-in) for person_id: {person_id} in slot {current_hour}:00")
            
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

def delete_user(person_id):
    """Delete a user and all associated data, including images."""
    session = get_session()
    try:
        person = session.query(Person).filter_by(id=person_id).first()
        if person:
            # Delete image directory if it exists
            # Assuming images are stored in enrollment_images/{person_id}
            # We need to import ENROLLMENT_DIR from config, but to avoid circular import issues if config imports database,
            # we can infer it or just check the image_path of the first encoding.
            
            # Better approach: Get one encoding to find the path
            enc = session.query(Encoding).filter_by(person_id=person_id).first()
            if enc and enc.image_path:
                user_dir = os.path.dirname(enc.image_path)
                if os.path.exists(user_dir):
                    try:
                        shutil.rmtree(user_dir)
                        logger.info(f"Deleted image directory: {user_dir}")
                    except Exception as e:
                        logger.error(f"Error deleting directory {user_dir}: {e}")

            session.delete(person)
            session.commit()
            logger.info(f"Deleted user: {person_id}")
            return True
        return False
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting user: {e}")
        return False
    finally:
        session.close()
