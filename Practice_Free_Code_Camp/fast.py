from fastapi import FastAPI
app= FastAPI()
# amazon.com/localhost/delete-user
# GET -GET AN INFORMATION
# post - CREATE SOMETHINGNEW
# put - UPDATE
# DELETE- DELETE SOMETHING
@app.get("/")
# def index():
#     return{"name":"First Data"}
# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
async def root():
    return {"message": "Hello World"}