from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


# Create a DeclarativeMeta instance
Base = declarative_base()


class DIRECTOR(Base):
    __tablename__ = "director"
    director_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    director_name = Column(String(80))


class COUNTRY(Base):
    __tablename__ = "country"
    country_id = Column(
        Integer, 
        nullable=False,
        primary_key=True, 
        autoincrement=True
    )
    country_name = Column(String(80))


class GENRE(Base):
    __tablename__ = "genre"
    genre_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    genre_name = Column(String(30))


class FILM(Base):
    __allow_unmapped__ = True
    __tablename__ = "film"
    film_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    title = Column(String(30))
    genre_id = Column(ForeignKey(GENRE.genre_id))
    country_id = Column(ForeignKey(COUNTRY.country_id))
    year_publication = Column(String(4))
    available_number = Column(Integer)


class FILM_DIRECTOR(Base):
    __tablename__ = "film_director"
    film_director_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    film_id = Column(ForeignKey(FILM.film_id))
    director_id = Column(ForeignKey(DIRECTOR.director_id))


class CLIENT(Base):
    __tablename__ = "client"
    client_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    client_name = Column(String(80))
    phone_number = Column(String(11))
    email_adress = Column(String(30))
    

class FILM_CLIENT(Base):
    __tablename__ = "film_client"
    film_client_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    film_id = Column(ForeignKey(FILM.film_id))
    client_id = Column(ForeignKey(CLIENT.client_id))
    borrow_date = Column(DateTime, default=datetime.now())
    return_date = Column(DateTime)


class MANAGER(Base):
    __tablename__ = "manager"
    manager_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    fullname = Column(String(80))
