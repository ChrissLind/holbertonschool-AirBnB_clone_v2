#!/usr/bin/python3
"""Module defines a class to manage Database storage for hbnb clone"""
import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review

os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'


class DBStorage:
    """Class for Database Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Engine"""
        self.__engine = db.create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns dictionary"""
        table_dict = {}
        classes = {
            'State': State, 'City': City,
            'User': User, 'Place': Place,
            }
        if cls is None:
            for c in classes:
                result = self.__session.query(classes[c]).all()
                for obj in result:
                    table_dict[f"{type(obj).__name__}.{obj.id}"] = obj
        else:
            result = self.__session.query(classes[cls]).all()
        for obj in result:
            table_dict[f"{type(obj).__name__}.{obj.id}"] = obj
        return table_dict

    def new(self, obj):
        """Adds to database"""
        self.__session.add(obj)

    def save(self):
        """Saves changes in session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from table"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads information from Database and starts Session"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(sess_factory)
        self.__session = session()
