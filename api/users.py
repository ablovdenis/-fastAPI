from data_storage_and_processing.configSQL import *
from data_storage_and_processing.schemas import *

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from typing import List

def user_exists(nickname): # Проверка на наличие юзера с таким ник-ом.
    for user in DataBase.query(UserModel).all():
        if nickname == user.nickname: return True
    return False
    

app = FastAPI()

current_user = []

@app.get('/admin/users', response_model=List[UserResponse])
def get_users():
    return DataBase.query(UserModel).all()

@app.get('/admin/user/{id}', response_model=UserResponse)
def get_detail(id: int):
    user = DataBase.get(UserModel, id)
    if user: return user
    else:
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким id не существует.'
        )

@app.get('/profile', response_model=UserProfileResponse)
def get_profile():
    if current_user:
        user = (DataBase.query(UserModel).
                filter(UserModel.nickname == current_user[0]).
                first())
        return user
    else:
        raise HTTPException(
            status_code=400,
            detail='Вы не вошли в аккаунт.'
        )

@app.get('/logout')
def logout_user():
    if current_user:
        current_user.clear()
        return PlainTextResponse(status_code=200, content='Вы вышли из аккаунта.')
    else:
        raise HTTPException(
            status_code=400,
            detail='Вы не были в аккаунте.'
        )

@app.delete('/admin/user/{id}')
def delete_user(id: int):
    user = DataBase.get(UserModel, id)
    if user:
        DataBase.delete(user)
        DataBase.commit()
        return PlainTextResponse(content='Пользователь удалён.')
    else:
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким id не существует.'
        )

@app.post('/login')
def create_user(data: UserRequest):
    if user_exists(data.nickname):
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким никнеймом уже существует.'
        )
    new_user = UserModel(nickname=data.nickname, password=data.password)
    DataBase.add(new_user)
    DataBase.commit()
    return PlainTextResponse(status_code=201, content='Пользователь авторизован.')

@app.post('/logon')
def logon_user(data: UserRequest):
    if current_user:
        raise HTTPException(
            status_code=400,
            detail='Вы уже вошли в аккаунт.'
        )
    if (user_exists(data.nickname) and
        data.password == (DataBase.query(UserModel).
                          filter(UserModel.nickname == data.nickname).
                          first().password)):
            current_user.append(data.nickname)
            return PlainTextResponse(status_code=200, content='Вход в аккаунт выполнен.')
    else:
        raise HTTPException(
            status_code=400,
            detail='Пароль неверный.'
        )

# @app.put('/users/{nickname}')
# def put_person(nickname: str, data: UserModel):
    # if nickname in DataBase:
        # data.created_at = DataBase[nickname].created_at
        # del DataBase[nickname]
        # DataBase[data.nickname] = data
    # else: raise HTTPException(
            # status_code=400,
            # detail='Пользователя с таким никнеймом не существует.'
        # )
    # return Response(
        # status_code=200, content='Данные о пользователе изменены.')

# @app.delete('/users/{nickname}')
# def delete_person(nickname: str):
    # if nickname in DataBase:
        # del DataBase[nickname]
        # return Response(content='Пользователь удалён')
    # else: raise HTTPException(
            # status_code=400,
            # detail='Пользователя с таким никнеймом не существует.'
        # )