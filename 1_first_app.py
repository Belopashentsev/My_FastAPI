from fastapi import FastAPI  # импортируем класс ФастАПИ

app = FastAPI()  # приложение - это экземпляр класса ФастАПИ


@app.get("/")
def hello():
    return "Hello World"

# прописываем вью функцию и декорируем её.
# декоратором указываем приложение
# далее прописываем метод и эндпоинт (в этом случае это корень)

# для запуска прописываем uvicorn main:app --reload
# где ювиконр - это локальный сервер, который запускает в файле мэйн.ру обьект арр
# параметр релоад автоматически будет перезапускать сервер при изменении кода.