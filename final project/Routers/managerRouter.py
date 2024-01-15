from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.database import *
from Database.schemas import *
from Models.model import *
from authorization import *

import json


# Create tables
Base.metadata.create_all(bind=engine)

manager_router = APIRouter(
    tags=["Manager"]
)


def verify_manager_role(role) -> bool:
    if role == "manager_role":
        return True
    else:
        return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------ Film managment ------------------------------------------------------

@manager_router.post("/addFilm")
def add_film(
    film_data: FilmModel,
    db: Session=Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Check authorization
    if not verify_manager_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Check that the id of the film being added does not exist
    film = db.query(FILM)\
            .filter(
                (FILM.title == film_data.title) &
                (FILM.genre_id == film_data.genre_id) &
                (FILM.country_id == film_data.country_id) &
                (FILM.year_publication == film_data.year_publication) &
                (FILM.available_number == film_data.available_number)
            )\
            .first()
    if film is not None:
        return JSONResponse(status_code=400, content="Film with current id number has already exist")
    
    # Check that the year of publication is not greater than the current one
    if int(film_data.year_publication) > datetime.now().year:
        return JSONResponse(
            status_code=400,
            content="The year of publication is > current one, or < 1900"
        )
    
    # Check that the genre is in the genre table
    # TODO: добавить сравнение по названию а не по id
    genre = db.query(GENRE)\
            .filter(GENRE.genre_id == film_data.genre_id)\
            .first()
    if genre is None:
        return JSONResponse(status_code=400, content="Genre does not exist")
    
    # Check that the country is in the country table
    # TODO: добавить сравнение по названию а не по id
    country = db.query(COUNTRY)\
             .filter(COUNTRY.country_id == film_data.country_id)\
             .first()
    if country is None:
        return JSONResponse(status_code=400, content="Country does not exist")
    
    # Check that the available_number >= 0
    if film_data.available_number < 0:
        return JSONResponse(status_code=400, content="The available number is not greater than zero")
    
    # Добавляем самолет
    film_to_add = FILM(
        title=film_data.title,
        genre_id=film_data.genre_id,
        country_id=film_data.country_id,
        year_publication=film_data.year_publication,
        available_number=film_data.available_number
    )
    db.add(film_to_add)
    db.commit()

    return {"message": "Film has been successfully added"}


@manager_router.put("/updateFilm")
def update_film_data(
    film_data: FilmModel,
    new_film_data: FilmModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Authorization check
    if not verify_manager_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Checking that the film's title is not empty
    if new_film_data.title == "":
        return JSONResponse(status_code=404, content={"message": "Film's title is empty"})
    
    # Checking available numbe >= 0:
    if new_film_data.available_number < 0:
        return JSONResponse(status_code=404, content={"message": "Available number < 0"})
    
    # Checking whether the genre_id is in the database:
    genre = db.query(GENRE)\
            .filter(GENRE.genre_id == new_film_data.genre_id)\
            .first()
    if genre is None:
        return JSONResponse(status_code=404, content={"message": "Genre is not found"})
    
    # Checking whether the country_id is in the database:
    country = db.query(COUNTRY)\
            .filter(COUNTRY.country_id == new_film_data.country_id)\
            .first()
    if country is None:
        return JSONResponse(status_code=404, content={"message": "Genre is not found"})
    
    # Check that the year of publication is not greater than the current one
    if int(new_film_data.year_publication) > datetime.now().year and\
        int(new_film_data.year_publication) < 1900:
        return JSONResponse(
            status_code=400,
            content="The year of publication is > current one, or < 1900"
        )

    # Checking whether the film is in the database
    film = db.query(FILM)\
                .filter(
                    (FILM.title == film_data.title) &
                    (FILM.genre_id == film_data.genre_id) &
                    (FILM.country_id == film_data.country_id) &
                    (FILM.year_publication == film_data.year_publication) &
                    (FILM.available_number == film_data.available_number)
                )\
                .first()
    if film is None:
        return JSONResponse(status_code=404, content={"message": "Film is not found"})
    
    # Update data
    film.title = new_film_data.title
    film.genre_id = new_film_data.genre_id
    film.country_id = new_film_data.country_id
    film.year_publication = new_film_data.year_publication
    film.available_number = new_film_data.available_number

    # Save changes
    db.commit()

    return {"message": "Film's data successfully updated"}


@manager_router.delete("/deleteFilm")
def delete_film(
    film_data: FilmModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Check authorization
    if not verify_manager_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Check that the film is in the film table
    film = db.query(FILM)\
            .filter(
                (FILM.title == film_data.title) &
                (FILM.genre_id == film_data.genre_id) &
                (FILM.country_id == film_data.country_id) &
                (FILM.year_publication == film_data.year_publication) &
                (FILM.available_number == film_data.available_number)     
            )\
            .first()
    if film is None:
        return JSONResponse(status_code=400, content="Film is not exist")
    
    db.delete(film)
    db.commit()

    return {"message": "Film has been successfully deleted"}


# ------------------------------------ Client management ------------------------------------------------------

@manager_router.post("/addClient")
def add_client(
    client_data: ClientModel,
    db: Session=Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Authorization check
    if not verify_manager_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Check client_name is not empty
    if client_data.client_name == "":
        return JSONResponse(status_code=400, content="The name of the client is empty")

    # Check client_email_adress is not empty
    if client_data.email_adress == "":
        return JSONResponse(status_code=400, content="The email adress of the client is empty")
    
    # Check phone_number is not empty
    if client_data.phone_number == "":
        return JSONResponse(status_code=400, content="The phone number of the client is empty")
    
    # Check that the client being added does not exist
    client = db.query(CLIENT)\
                .filter(
                    (CLIENT.client_name == client_data.client_name) &
                    (CLIENT.email_adress == client_data.email_adress) &
                    (CLIENT.phone_number == client_data.phone_number)
                )\
                .first()
    if client is not None:
        return JSONResponse(status_code=400, content="Client has already exist")
    
    # Add client
    client_to_add = CLIENT(
        client_name=client_data.client_name,
        phone_number=client_data.phone_number,
        email_adress=client_data.email_adress
    )
    db.add(client_to_add)
    db.commit()

    return {"message": "Client has been successfully added"}


@manager_router.put("/updateClient")
def update_client_data(
    client_data: ClientModel,
    new_client_data: ClientModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Checking whether the client is in the database
    client = db.query(CLIENT)\
                .filter(
                    (CLIENT.client_name == client_data.client_name) &
                    (CLIENT.phone_number == client_data.phone_number) &
                    (CLIENT.email_adress == client_data.email_adress)
                )\
                .first()
    if client is None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})
    
    # Authorization check
    if not verify_manager_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Checking that the client name is not empty
    if new_client_data.client_name == "":
        return JSONResponse(status_code=404, content={"message": "Client name is empty"})
    
    # Checking phone number is not empty:
    if new_client_data.phone_number == "":
        return JSONResponse(status_code=404, content={"message": "Phone number is empty"})
    
    # Checking email adress is not empty:
    if new_client_data.email_adress == "":
        return JSONResponse(status_code=404, content={"message": "Email adress is empty"})
    
    # Update data
    client.client_name = new_client_data.client_name
    client.phone_number = new_client_data.phone_number
    client.email_adress = new_client_data.email_adress
    
    # Save changes
    db.commit()

    return {"message": "Film's data successfully updated"}


@manager_router.delete("/deleteClient")
def delete_client(
    client_data: ClientModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Check authorization
    if not verify_manager_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Check that the client is in the client table
    client = db.query(CLIENT)\
            .filter(
                (CLIENT.client_name == client_data.client_name) &
                (CLIENT.phone_number == client_data.phone_number) &
                (CLIENT.email_adress == client_data.email_adress)    
            )\
            .first()
    if client is None:
        return JSONResponse(status_code=400, content="Client is not exist")
    
    db.delete(client)
    db.commit()

    return {"message": "Client has been successfully deleted"}
