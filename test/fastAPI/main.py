from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    email: str


app = FastAPI(title="Person API", description="Testing-only in-memory CRUD API")

people: Dict[int, Person] = {}

def to_dict(model: BaseModel) -> dict:
    return model.model_dump()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/people", response_model=List[Person])
async def read_people():
    print(f"READ: requested all people; current data: {[to_dict(p) for p in people.values()]}")
    return list(people.values())


@app.get("/people/{person_id}", response_model=Person)
async def read_person(person_id: int):
    person = people.get(person_id)
    if person is None:
        print(f"READ: person {person_id} not found")
        raise HTTPException(status_code=404, detail="Person not found")

    print(f"READ: person {person_id} returned data: {to_dict(person)}")
    return person


@app.post("/people", response_model=Person, status_code=status.HTTP_201_CREATED)
async def create_person(person: Person):
    if person.id in people:
        print(f"CREATE: rejected duplicate person with id {person.id} and data {to_dict(person)}")
        raise HTTPException(status_code=400, detail="Person already exists")

    people[person.id] = person
    print(f"CREATE: received data {to_dict(person)} and created a new person")
    return person


@app.put("/people/{person_id}", response_model=Person)
async def update_person(person_id: int, person: Person):
    if person_id != person.id:
        print(f"UPDATE: mismatch between path id {person_id} and payload id {person.id}")
        raise HTTPException(status_code=400, detail="Path id and payload id must match")

    if person_id not in people:
        print(f"UPDATE: cannot update missing person {person_id} with data {to_dict(person)}")
        raise HTTPException(status_code=404, detail="Person not found")

    people[person_id] = person
    print(f"UPDATE: updated person {person_id} with data {to_dict(person)}")
    return person


@app.delete("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(person_id: int):
    person = people.get(person_id)
    if person is None:
        print(f"DELETE: person {person_id} not found")
        raise HTTPException(status_code=404, detail="Person not found")

    del people[person_id]
    print(f"DELETE: removed person {person_id} with data {to_dict(person)}")
    return None