from pydantic import BaseModel, Field, field_validator, computed_field
from functools import cached_property
from datetime import datetime as dati

class Create_atModel(BaseModel):
    @computed_field # Это для автоматического подсчёта поля создания.
    @cached_property # Это для запрета повторного вычисления (чтоб не обновлялось при
                     # get и put запросах.
    def created_at(self) -> dati:
        return dati.now()

class UserModel(Create_atModel):
    nickname: str = Field(min_length=4, max_length=30)
    password: str = Field(exclude=True, min_length=10, max_length=40)
    @field_validator('password')
    def check_password(cls, value):
        contains_numbers = False
        contains_symbols = False
        for character in value:
            if character.isdigit(): contains_numbers = True
            elif character.isalpha(): contains_symbols = True
            if contains_numbers and contains_symbols: break
        if not(contains_numbers and contains_symbols and '!' in value and
               '#' in value) or ' ' in value:
            raise ValueError('Пароль должен содержать цифры, символы латиницы, знаки \'!\' и \'#\' и не должен содержать пробелы.')
        return value

class MyBaseModel(Create_atModel):
    if_published: bool = Field(
        default=True, description='Снимите галочку, чтобы скрыть публикацию.'
    )

class Post(MyBaseModel):
    title: str = Field(max_length=256, alias='Заголовок')
    text: str = Field(alias='Текст')
    pub_date: dati = Field(
        alias='Дата и время публикации',
        description=('Если установить дату и время в будущем'
                     ' — можно делать отложенные публикации.')
    )
    author: UserModel = Field(alias='Автор публикации')
    location: LocationModel = Field(default=None, alias='Местоположение')
    category: CategoryModel = Field(alias='Категория')
    # image: ImageField = Field(default=None)

class CategoryModel(MyBaseModel):
    title: str = Field(max_length=256, alias='Заголовок')
    description: str = Field(alias='Описание')
    slug: str = Field(
        alias='Идентификатор',
        description=('Идентификатор страницы для URL; разрешены'
                     ' символы латиницы, цифры, дефис и подчёркивание.')
    )

class LocationModel(MyBaseModel):
    name: str = Field(max_length=256, alias='Название места')


class CommentModel(Create_atModel):
    text: str = Field(alias='Текст комментария')
    post: str = Field(alias='Комментарий')
    author: UserModel