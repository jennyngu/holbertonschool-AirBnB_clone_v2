#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, ForeignKey

Base = declarative_base()


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), primary_key=True,
                             ForeignKey=places.id, nullable=False),
                      Column('amenity_id', String(60), primary_key=True,
                             ForeignKey=amenities.id, nullable=False)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True, default=0.0)
    longitude = Column(Float nullable=True, default=0.0)
    amenity_ids = []

    amenities = relationship('Amenity', secondary=place_amenity, viewonly=False)

    @property
    def amenities(self):
        amenity_list = []
        all_amenities = FileStorage().all(Amenity)
        for amenity_id in self.amenity_ids:
            for amenity in all_amenities.values():
                if amenity.id == amenity_id:
                    amenity_list.append(amenity)
                    break
        return amenity_list

    @amenities.setter
    def amenities(self, amenity_obj):
        if isinstance(amenity_obj, Amenity):
            self.amenity_ids.append(amenity_obj.id)
