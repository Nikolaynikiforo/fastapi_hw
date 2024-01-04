from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return "Welcome to Vet information service!"


@app.post('/post')
def get_post() -> Timestamp:
    new_timestamp = Timestamp(id=max([timestamp.id for timestamp in post_db]) + 1,
                              timestamp=time.time_ns())
    post_db.append(new_timestamp)
    return new_timestamp


@app.get('/dog')
def get_dogs(kind: DogType = None) -> List[Dog]:
    if kind is None:
        return [dogs_db[i] for i in dogs_db.keys()]
    return [dogs_db[i] for i in dogs_db.keys() if dogs_db[i].kind == kind]


@app.post('/dog')
def create_dog(new_dog: Dog) -> Dog:
    new_pk = max(dogs_db.keys()) + 1
    new_dog.pk = new_pk
    dogs_db[new_pk] = new_dog

    new_timestamp = Timestamp(id=max([timestamp.id for timestamp in post_db]) + 1,
                              timestamp=time.time_ns())
    post_db.append(new_timestamp)

    return new_dog

@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="No dog with such primary key")

    return dogs_db[pk]


@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="No dog with such primary key")
    dogs_db[pk] = dog

    new_timestamp = Timestamp(id=max([timestamp.id for timestamp in post_db]) + 1,
                              timestamp=time.time_ns())
    post_db.append(new_timestamp)

    return dog
