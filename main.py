from models.models import InheritanceModel
from fastapi import FastAPI
from fastapi.responses import Response

DB = []
 
app = FastAPI()
 
@app.get("/users")
def get_people():
    return DB
 
@app.post("/users")
def create_person(data  = InheritanceModel):
    DB.append(data)
    return Response(status_code=201)