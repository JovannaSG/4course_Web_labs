from pydantic import BaseModel, Field


class KeycloakToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    not_before_policy: int = Field(alias="not-before-policy")
    session_state: str
    scope: str


class ClientModel(BaseModel):
    client_name: str
    phone_number: str
    email_adress: str


class FilmModel(BaseModel):
    title: str
    genre_id: int
    country_id: int
    year_publication: str
    available_number: int


class ManagerModel(BaseModel):
    manager_id: int
    fullname: str


class DirectorModel(BaseModel):
    director_id: int
    director_name: str


class CountryModel(BaseModel):
    country_id: int
    country_name: str


class GenreModel(BaseModel):
    genre_id: int
    genre_name: str


class FilmClientModel(BaseModel):
    # film_client_id: int
    film_id: int
    client_id: int
    borrow_date: str 
    return_date: str  
