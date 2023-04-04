#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models
    """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Instantiates a new model
        """
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            storage.new(self)
        else:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
            self.created_at = datetime.strptime(self.created_at,
                                                '%Y-%m-%dT%H:%M:%S.%f')
            self.updated_at = datetime.strptime(self.updated_at,
                                                '%Y-%m-%dT%H:%M:%S.%f')
            if not hasattr(self, 'id'):
                self.id = str(uuid.uuid4())


    def __str__(self):
        """
        Returns a string representation of the instance
        """
        classname = self.__class__.__name__
        d = self.__dict__.copy()
        d.pop('_sa_instance_state', None)
        return "[{}] ({}) {}".format(classname, self.id, d)

    def save(self):
        """
        Updates updated_at with current time when instance is changed
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.save()

    def to_dict(self):
        """
        Convert instance into dict format
        """
        d = self.__dict__.copy()
        d.pop('_sa_instance_state', None)
        d["__class__"] = self.__class__.__name__
        d["created_at"] = self.created_at.isoformat()
        d["updated_at"] = self.updated_at.isoformat()
        return d

    def delete(self):
        """
        Deletes the current instance from the storage
        """
        from models import storage

        storage.delete(self)
