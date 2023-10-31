from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Table, create_engine, MetaData, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.config import DATABASE_URL
import uuid

# Initialize the database
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()

# Mixin for audit _at columns
class AuditMixinAt:
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Mixin for audit _by columns
class AuditMixinBy:
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    modified_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))

# Many-to-Many association table between Users and Hangouts
participants = Table('participants', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('hangout_id', UUID(as_uuid=True), ForeignKey('hangouts.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('modified_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('modified_by', UUID(as_uuid=True), ForeignKey('users.id'))
)

# Many-to-Many association table between Expenses and Users who share the expense
expense_shared_by = Table('expense_shared_by', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('expense_id', UUID(as_uuid=True), ForeignKey('expenses.id'), primary_key=True)
)

class User(Base, AuditMixinAt):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(225), nullable=False)
    avatar = Column(String(1000))
    
    # Relationships
    hangouts = relationship(
        "Hangout",
        secondary=participants,
        primaryjoin="User.id==participants.c.user_id",
        secondaryjoin="Hangout.id==participants.c.hangout_id",
        back_populates="users"
    )
    shared_expenses = relationship(
        "Expense",
        secondary=expense_shared_by,
        primaryjoin="User.id==expense_shared_by.c.user_id",
        secondaryjoin="Expense.id==expense_shared_by.c.expense_id",
        back_populates="shared_by"
    )
    comments = relationship("Comment", primaryjoin="User.id==Comment.author_id", back_populates="author")

class Hangout(Base, AuditMixinAt, AuditMixinBy):
    __tablename__ = 'hangouts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    location = Column(String(225), nullable=False)
    time = Column(DateTime, nullable=False)
    notes = Column(String(500))

    # Relationships
    users = relationship(
        "User",
        secondary=participants,
        primaryjoin="Hangout.id==participants.c.hangout_id",
        secondaryjoin="User.id==participants.c.user_id",
        back_populates="hangouts"
    )
    expenses = relationship("Expense", back_populates="hangout")
    comments = relationship("Comment", back_populates="hangout")

class Expense(Base, AuditMixinAt, AuditMixinBy):
    __tablename__ = 'expenses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    hangout_id = Column(UUID(as_uuid=True), ForeignKey('hangouts.id'), nullable=False)
    amount = Column(Integer, nullable=False)

    # Relationships
    hangout = relationship("Hangout", back_populates="expenses")
    shared_by = relationship(
        "User",
        secondary=expense_shared_by,
        primaryjoin="Expense.id==expense_shared_by.c.expense_id",
        secondaryjoin="User.id==expense_shared_by.c.user_id",
        back_populates="shared_expenses"
    )

class Comment(Base, AuditMixinAt, AuditMixinBy):
    __tablename__ = 'comments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    hangout_id = Column(UUID(as_uuid=True), ForeignKey('hangouts.id'), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    text = Column(String(225), nullable=False)
    
    # Relationships
    hangout = relationship("Hangout", back_populates="comments")
    author = relationship("User", primaryjoin="User.id==Comment.author_id", back_populates="comments")
