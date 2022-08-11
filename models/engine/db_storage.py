#!/usr/bin/python3
"""Defines a DBStorage engine."""
from models.base_model import Base, BaseModel
from os import getenv
from models.city import City
from models.state import State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship


class DBStorage:
    """Represents a database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        if cls is None:
            obj = self.__session.query(State).all()
            obj.extend(self.__session.query(City).all())
        else:
            if type(cls) == str:
                eval(cls)
            obj = self.__session.query(cls).all()
            return {"{}.{}".format(type(o).__name__, o.id): o for o in obj}

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_now = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_now)
        self.__session = Session
