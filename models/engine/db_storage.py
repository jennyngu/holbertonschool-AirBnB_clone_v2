#!/usr/bin/python3
"""This module defines a database storage engine"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """The engine that handles the database storage"""

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine instance and starts the session"""
        user = os.environ.get('HBNB_MYSQL_USER')
        pwd = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        db = os.environ.get('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

        Base.metadata.create_all(bind=self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Returns a dictionary of all objects of a certain class"""
        objs = {}

        if cls is None:
            classes = [BaseModel, State, City]  # Add the new classes here
        else:
            classes = [cls]

        for c in classes:
            for obj in self.__session.query(c).all():
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objs[key] = obj

        return objs

    def new(self, obj):
        """Adds an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(bind=self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        self.__session.remove()
        self.__session.close_all()
