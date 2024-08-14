#!/usr/bin/env python3
""" User model
Defines a User model for SQLAlchemy ORM.
"""

# Import necessary modules from SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Create a base class for models
Base = declarative_base()


class User(Base):
    """ SQLAlchemy User model
         Represents a user in the database with fields for id, email,
         hashed_password, session_id, and reset_token.
    """
    # Define the table name
    __tablename__ = 'users'

    # Define columns for the User model
    id = Column(Integer, primary_key=True)
    # Email column, maximum length 250 characters, cannot be null
    email = Column(String(250), nullable=False)
    # Hashed password column, maximum length 250 characters, cannot be null
    hashed_password = Column(String(250), nullable=False)
    # Session ID column, maximum length 250 characters, can be null
    session_id = Column(String(250), nullable=True)
    # Reset token column, maximum length 250 characters, can be null
    reset_token = Column(String(250), nullable=True)
