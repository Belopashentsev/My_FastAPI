from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI  # импортируем класс ФастАПИ
from pydantic import BaseModel, Field

# приложение - это экземпляр класса ФастАПИ, в параметрах указываем название приложения
app = FastAPI(
    title="Trading APP"
    )



# валидация нужна для проверки получаемых и отправляемых данных на соответствие ожидаемому формату и типу


users_db = [
    {'id': 1, 'role': "admin", 'name': 'Bob'},
    {'id': 2, 'role': "investor", 'name': 'Sam'},
    {'id': 3, 'role': "trader", 'name': 'Joe'},
    {'id': 4, 'role': "trader", 'name': 'Mike', 'degree':[
        {'id': 1, 'created_at': "2023-07-05T13:27:39.630Z", 'type_degree': 'expert'}
        ]},
    ]


# опишем возможные типы званий
class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


# опишем класс званий
class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


# опишем модель данных Юзера
class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[list[Degree]] = [] # либо список званий, либо пустой список


# для валидации отправляемых данных укажем бодель ответа в качестве параметра декоратора:
@app.get('/users/{user_id}', response_model=list[User]) # фигурные скобки создают переменную
def get_user(user_id: int): # аннотация преобразует тип данных
    return [user for user in users_db if user['id'] == user_id]


trades_db = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 122, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
    ]


@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0): # лимит - максимум записей в JSON, оффсет - сдвиг для пагинации
    return trades_db[offset:][:limit] # см работу со списками по индексам


# допустим мы ходим добавить сделку в список, при этом вручную прописывать параметры модели в запросе не удобно.
# что бы упростить - пропишем модель используя Пайдентик:


# создадим класс, унаследованный от класса БейсМодел из Пайдентика и опишем модель
# для валидации получаемых данных сделки:
class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5) # поле с максимальной длиной 5 символов
    side: str
    price: float = Field(ge=0) # поле со значением greated equal 0 (больше или равно)
    amount: float


# в аннотации укажем, что ожидается список с экземплярами класса Трейд
@app.post('/trades')
def add_trades(trades: list[Trade]):
    trades_db.append(trades)
    return {'status': 200, 'data': trades_db}