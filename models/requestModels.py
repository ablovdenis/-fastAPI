from pydantic import BaseModel, Field, field_validator, computed_field
from functools import cached_property
from datetime import datetime as dati

class UserModel(BaseModel):
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
               '#' in value):
            raise ValueError('Пароль должен содержать цифры, символы латиницы, знаки \'!\' и \'#\' и не должен содержать пробелы.')
        return value
    # created_at: dati = Field(default=dati.now())
    @computed_field # Это для автоматического подсчёта поля создания.
    @cached_property # Это для запрета повторного вычисления (чтоб не обновлялось при
                     # get и put запросах.
    def created_at(self) -> dati:
        return dati.now()

# class MyBaseModel(BaseModel):
    # if_published: bool = Field(
        # default=True, description='Снимите галочку, чтобы скрыть публикацию.'
    # )
    # @computed_field
    # def created_at(self):
        # return date.today()