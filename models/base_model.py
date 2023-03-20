#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            self.created_at = datetime.strptime(self.created_at,
                                                '%Y-%m-%dT%H:%M:%S.%f')
            self.updated_at = datetime.strptime(self.updated_at,
                                                '%Y-%m-%dT%H:%M:%S.%f')
            if not self.id:
                self.id = str(uuid.uuid4())
            if not self.created_at:
                self.created_at = datetime.now()
            if not self.updated_at:
                self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = type(self).__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes the current instance from storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary['__class__'] = type(self).__name__
        dictionary.pop('_sa_instance_state', None)
        return dictionary
