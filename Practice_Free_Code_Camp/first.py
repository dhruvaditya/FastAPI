from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class Post(BaseModel):
    title:str
    content: str

@app.get("/")
def index():
    return {"Name": " Aditya Raj"}
student={
        1:{
            "Name": "Shishir ",
            "Tech":"iOS"
        },
        2:{
            "Name":"Vivek",
            "Tech":"AI"
        }
    }
@app.get("get-student/{student_id}")
def get_student(student_id:int):
    return student[student_id]
@app.get("/posts")
def getpostas():
    return {"get post":"This is our post"}
@app.get("/createposts")
def createposts(new_post:Post):
    print(new_post.title)
    return{"data":"new post"}
    