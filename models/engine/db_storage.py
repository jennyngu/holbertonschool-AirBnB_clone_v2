#!/usr/bin/python3
"""
This module defines the DBStorage class.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base


class DBStorage:
    """This class manages storage of hbnb models in a MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Create a new instance of DBStorage."""
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        db = os.environ.get('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, db),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session (self.__session) all objects
        depending of the class name (argument cls).
        If cls=None, query all types of objects (User, State, City, Amenity,
        Place and Review).
        Return:
            Returns a dictionary of all objects in the database of a
            certain class, or all classes if no class is passed.
        """
        if cls is not None:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for c in Base.__subclasses__():
                objs += self.__session.query(c).all()
        return {'{}.{}'.format(type(obj).__name__, obj.id): obj for obj in objs}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()
