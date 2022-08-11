#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref='State', cascade="delete")
    else:
        @property
        def cities_att(self):
            """Defines cities attribute for FileStorage"""
            from models import storage
            cities_dict = storage.all('City')
            cities_list = []
            for key, value in cities_dict.items():
                if value.state_id == self.id:
                    cities_list.append(value)
            return cities_list
