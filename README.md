# Сервис объявлений на FastAPI

REST API сервис для размещения и поиска объявлений о купле/продаже.
Проект выполнен в рамках домашнего задания.

## Функционал

- Создание объявления (POST)
- Просмотр объявления по ID (GET)
- Поиск объявлений по заголовку и цене (GET)
- Обновление объявления (PATCH)
- Удаление объявления (DELETE)

## Технологии

- Python 3.9
- FastAPI
- Pydantic
- Docker

## Запуск локально

1. **Клонируйте репозиторий:**
   ```bash
   git clone git@github.com:Edo19999/REST-API-on-FastApi.git
   cd "REST API on FastApi"
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/MacOS:
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите сервер:**
   ```bash
   uvicorn main:app --reload
   ```
   Сервер будет доступен по адресу: http://127.0.0.1:8000
   Документация (Swagger): http://127.0.0.1:8000/docs

## Запуск через Docker

1. **Соберите образ:**
   ```bash
   docker build -t advertisement-app .
   ```

2. **Запустите контейнер:**
   ```bash
   docker run -p 8000:8000 advertisement-app
   ```
