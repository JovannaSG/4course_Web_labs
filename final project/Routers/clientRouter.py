from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.database import *
from Database.schemas import *
from Models.model import *
from authorization import KeycloakJWTBearerHandler, HTTPException

import json


# create tables
Base.metadata.create_all(bind=engine)

client_router = APIRouter(
    tags=["Client"]
)


def verify_client_role(role) -> bool:
    if role == "client_role":
        return True
    return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@client_router.post("/takeFilm")
def take_film(
    film_name: str,
    film_data: FilmClientModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Authorization check
    if not verify_client_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Check that film exist in film table
    check_film = db.query(FILM)\
                    .filter(FILM.title == film_name)\
                    .first()
    if check_film is None:
        raise HTTPException(status=404, detail={"message": "Film not found"})
    
    # Create film and add in DB
    film = FILM_CLIENT(
        film_id=check_film.film_id,
        client_id=film_data.client_id,
        borrow_date=datetime.strptime(film_data.borrow_date, '%Y-%m-%d'),
        return_date=datetime.now() #strptime(film_data.return_date, '%Y-%m-%d')
    )
    db.add(film)
    db.commit()
    
    update_available_number = db.query(FILM)\
                                .filter(FILM.film_id == check_film.film_id)\
                                .first()
    upd_number = FILM(
        title=update_available_number.title,
        genre_id=update_available_number.genre_id,
        country_id=update_available_number.country_id,
        year_publication=update_available_number.year_publication,
        available_number=update_available_number.available_number - 1
    )
    db.add(upd_number)
    db.commit()
    
    return {"message": "Film was successfully taken"}


@client_router.post("/getClientFilms")
def get_client_films(
    client_data: ClientModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Authorization check
    if not verify_client_role(role):
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
        return JSONResponse(status_code=404, content={"message": "Client is not found"})
    
    # Find films purchased by the client
    # Check that client exist
    qr = db.query(CLIENT)\
                .filter(
                    (CLIENT.client_name == client_data.client_name) &
                    (CLIENT.phone_number == client_data.phone_number) &
                    (CLIENT.email_adress == client_data.email_adress)
                )\
                .first()
    # Get all client's films
    films = db.query(FILM_CLIENT)\
                .filter(FILM_CLIENT.client_id == qr.client_id)\
                .all()
    data = dict()
    data["films"] = list()
    for f in films:
        d = dict()
        d["film_client_id"] = f.film_client_id
        d["film_id"] = f.film_id
        d["client_id"] = f.client_id
        d["borrow_date"] = f.borrow_date
        d["return_date"] = f.return_date
        data["films"].append(d)

    return json.loads(json.dumps(data, default=str))


@client_router.delete("/delFilm")
def delete_film(
    client_data: FilmClientModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Authorazation check
    if not verify_client_role(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Checking whether the client is in the database
    client = db.query(CLIENT)\
                    .filter(
                        (CLIENT.client_id == client_data.client_id) &
                        (FILM_CLIENT.borrow_date == client_data.borrow_date) &
                        (FILM_CLIENT.return_date == client_data.return_date)
                    )\
                    .first()
    if client is None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})
    
    # Check whether there is a purchased film in film_client table
    film = db.query(FILM_CLIENT)\
               .filter(
                    (FILM_CLIENT.film_id == client_data.film_id) &\
                    (FILM_CLIENT.client_id == client_data.client_id)
                )\
               .first()
    if film is None:
        return JSONResponse(status_code=404, content={"message": "Film is not found"})
    
    db.delete(film)
    db.commit()

    return {"message": "Film deleted successfully"}
