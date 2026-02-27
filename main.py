from models import requestModels, responseModels
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

DataBase = {} # Модель базы данных.
              # Сделал словарь, чтоб быстрее проверять коллизии имён при
              # попытках создания и изменения никнейма.

def nicknames_collision(nickname): # Проверка на наличие юзера с таким ник-ом.
    if nickname in DataBase:
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким никнеймом уже существует.'
        )

app = FastAPI()
 
@app.get('/users')
def get_people():
    lstDB = []
    for elem in DataBase.values():
        lstDB.append(elem)
    return lstDB

@app.get('/users/{nickname}')
def get_detail(nickname: str):
    if nickname in DataBase: return DataBase[nickname]
    else: raise HTTPException(
            status_code=400,
            detail='Пользователя с таким никнеймом не существует.'
        )
 
@app.post('/users')
def create_person(data: requestModels.UserModel):
    nicknames_collision(data.nickname)
    DataBase[data.nickname] = data
    return Response(status_code=201, content='Создан новый пользователь.')

@app.put('/users/{nickname}')
def put_person(nickname: str, data: requestModels.UserModel):
    if nickname in DataBase:
        data.created_at = DataBase[nickname].created_at
        DataBase[data.nickname] = data
        del DataBase[nickname]
    else: raise HTTPException(
            status_code=400,
            detail='Пользователя с таким никнеймом не существует.'
        )
    return Response(
        status_code=200, content='Данные о пользователе изменены.')

@app.delete('/users/{nickname}')
def delete_person(nickname: str):
    if nickname in DataBase: del DataBase[nickname]
    else: raise HTTPException(
            status_code=400,
            detail='Пользователя с таким никнеймом не существует.'
        )
    return Response(status_code=204, content='Пользователь удалён.')