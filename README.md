# it_megastar_task
Сервис, который хранит в PostgreSQL данные о писателях и их книгах, и умеет по HTTP-запросу GET /writers/&lt;writer_id>  возвращать информацию о писателе и его книгах в формате (JSON)

Иницализация базы данных производится в файле main.py в строке, где указан ключ SQLALCHEMY_DATABASE_URI.
'postgresql://login:password@host:port/db_name'

перед запуском сервиса установить все необходимые библиотеки: pip install -r requirements.txt

запуск сервиса производится из командной строки с параметром init: python main.py init
