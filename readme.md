## Памятка
Создание миграции

    alembic revision --autogenerate -m "название миграции"

команда выполнит операции обновления, исходя из текущей версии базы данных  , к заданной целевой редакции head тоесть последней

    alembic upgrade head

Если база данных пустая или еще какието приколы с бд незнаю что делает но иногда помогает

    alembic stamp head

 Запускать бекенд так (команда повершелл)

    alembic upgrade head;uvicorn backend.main:app --host localhost --port 3000

 Запускать фронтенд так (команда повершелл)
    cd .\frontend\; npm run dev

разберу подребней запуск сервера `uvicorn main:app --host 0.0.0.0 --port 3000`
`main` - название файла
`app` - экземпляр fastapi в этом файле
`--host 0.0.0.0` - адрес сервера 0.0.0.0 это локалхост 
`--port 3000` - порт

чтоб запустить на пустой базе данных раскоментируй строчку в файле
backend/db/session.py
чтоб не писало что связей нет
это их создаст

`Base.metadata.create_all(engine)`

на следущие запуски закоментруй


