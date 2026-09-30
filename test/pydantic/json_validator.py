import pathlib
from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr
    
json_string = pathlib.Path('wrong.json').read_text()
try:
    person = Person.model_validate_json(json_string)
    print(person)
except Exception as e:
    print(f"Validation error: {e}")