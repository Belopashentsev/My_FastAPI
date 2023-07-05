from fastapi import FastAPI  # импортируем класс ФастАПИ

# приложение - это экземпляр класса ФастАПИ, в параметрах указываем название приложения
app = FastAPI(
    title="Trading APP"
    )



# ЭНДПОИНТЫ:
# имитируем базу данных с пользователями:
users_db = [
    {'id': 1, 'role': "admin", 'name': 'Bob'},
    {'id': 2, 'role': "investor", 'name': 'Sam'},
    {'id': 3, 'role': "trader", 'name': 'Joe'},
    ]

# допустим мы хотим просмотреть данные пользователя:
@app.get('/users/{user_id}') # фигурные скобки создают переменную
def get_user(user_id: int): # аннотация преобразует тип данных
    return [user for user in users_db if user['id'] == user_id]



# ПАРАМЕТРЫ:
# имитируем базу данных со сделками:
trades_db = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 122, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
    ]

# допустим мы хотим получить список сделок:
@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0): # лимит - максимум записей в JSON, оффсет - сдвиг для пагинации
    return trades_db[offset:][:limit] # см работу со списками по индексам



# КОМБИНИРУЕМ
# имитируем базу данных с пользователями для POST:
users_db_2 = [
    {'id': 1, 'role': "admin", 'name': 'Bob'},
    {'id': 2, 'role': "investor", 'name': 'Sam'},
    {'id': 3, 'role': "trader", 'name': 'Joe'},
    ]

# допустим мы хотим изменить имя пользователя:
@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, users_db_2))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}





#     УРОК 2 "Эндпоинты, Параметры URL и Запроса"


# Эндпоинты
#
# 1. @app.get('/users/{user_id}') - заключенный в фигурные скобки эндпоинт является переменной,
#     значение в ней по умолчанию строка
# 2. def get_user(user_id: int): указывая аннотацию мы влияем на тип содержимого переменной,
#     то есть в данном случае автоматически преобразуем str в int


# Параметры URL
#
# 1. def get_trades(limit: int = 1, offset: int = 0) аргументы, указанные в функции,
#     становятся параметрами запроса: http://127.0.0.1:8000/trades?limit=1&offset=0
# 2. если не заданы аргументы по умолчанию, то это будут обязательные параметры, иначе
#     запрос будет сделан с указанными параметрами
# 3. ответ всегда преобразуется фреймворком в формат JSON согласно требованиям REST API


# Изменение имени пользователя
#
# 1. укажем в декораторе метод пост, эндпоинт будет тот же, что и при получении юзера
# 2. найдем в базе нужного юзера и переприсвоим имя
# 3. вернем словарь с успешным кодом и самого юзера
# 4. def change_user_name(user_id: int, new_name: str) потребует ввести айди и новое имя
# 5. будет сделан пост запрос с параметрами http://127.0.0.1:8000/users/1?new_name=Samanta