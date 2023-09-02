from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()


# Many-to-Many association table between Users and Hangouts
participants = Table('participants', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('hangout_id', UUID(as_uuid=True), ForeignKey('hangouts.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('modified_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('modified_by', UUID(as_uuid=True), ForeignKey('users.id'))
)

# Many-to-Many association table between Expenses and Users
expense_participants = Table('expense_participants', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('expense_id', UUID(as_uuid=True), ForeignKey('expenses.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('modified_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('modified_by', UUID(as_uuid=True), ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(225), nullable=False)
    avatar = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    hangouts = relationship("Hangout", secondary=participants, back_populates="participants")

class Hangout(Base):
    __tablename__ = 'hangouts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    location = Column(String(225), nullable=False)
    time = Column(DateTime, nullable=False)
    notes = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    modified_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    # Relationships
    participants = relationship("User", secondary=participants, back_populates="hangouts")
    expenses = relationship("Expenses", back_populates="hangout")

class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    hangout_id = Column(UUID(as_uuid=True), ForeignKey('hangouts.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    modified_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    # Relationships
    hangout = relationship("Hangout", back_populates="expenses")


# Initialize the database
engine = create_engine("postgresql://username:password@localhost/dbname")
Base.metadata.create_all(engine)
