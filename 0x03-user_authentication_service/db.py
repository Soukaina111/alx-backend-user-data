#!/usr/bin/env python3
"""
DB module for database operations
Handles all interactions with the database,
including initialization, session management, and CRUD operations for users.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    DB class for managing database connections and operations
    Attributes:
    engine (Engine): SQLAlchemy engine instance connected to the database.
    __session (Session): SQLAlchemy ORM session
    instance for database operations.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        Initializes the database engine,
        creates all tables based on the models,
        and prepares the session for database operations.
        """

        self._engine = create_engine(
            "sqlite:///a.db",
            connect_args={
                "check_same_thread": False})
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Lazy-loaded session property
        Returns a SQLAlchemy ORM session instance bound to the engine.
        Creates a new session if one does not exist.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
            return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        Returns:
        User: The newly added user instance.
        Adds a new user record to
        the database and commits the transaction.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user based on given criteria
        Args:
        **kwargs: Search criteria for finding a user.
        Returns:
        User: The found user instance
        Raises NoResultFound if no matching user is found.
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's details
        Raises ValueError if the update
        fails due to invalid criteria or missing fields.
        Finds a user by ID, updates the
        specified fields, and commits the changes.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise InvalidRequestError
                self._session.commit()
        except (NoResultFound, InvalidRequestError):
            raise ValueError("Failed to update user")
