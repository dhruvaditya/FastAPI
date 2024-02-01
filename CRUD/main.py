from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
@app.get("/",status_code=200)
class Person(BaseModel):
    id: int
    firstnamer: str
    lastname: str
    isMale: bool
@app.get("/person_info/{person_id}",status_code=200)
def person_info(person_id:int):
    return {"person id": f"Person id is {person_id}"}
@app.post("/add_person",status_code=200)
def add_person_info(person:Person):
    return{
        "id":person.id,
        "first name":person.firstnamer,
        "last name":person.lastname,
        "isMale":true

    }
