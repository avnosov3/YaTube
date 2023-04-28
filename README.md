# [YaTube](https://budiroga.pythonanywhere.com/)
[YaTube](https://budiroga.pythonanywhere.com/) - социальная сеть, в которой реализована возможность публикации и комментирования постов,
подписки на авторов. В проекте использована пагинация и кеширование страниц. Написаны
тесты для проверки реализованных функций сайта и подключен django-debug-toolbar. Дополнительно разработан REST [API](https://budiroga.pythonanywhere.com/api/v1/redoc/) для сервиса [(документация API)](https://budiroga.pythonanywhere.com/api/v1/redoc/).

## Техно-стек
* python 3.7.9
* django 2.2.16
* drf 3.12.4
* drf-simlejwt 4.7.2
* djoser 2.1.0
* django-debug-toolbar 3.2.4
* pillow 8.3.1
* sorl-thumbnail 12.7.0
* postgres 13.0
* gunicorn 20.0.4
* nginx 1.21.3

## Запуск проекта
1. Клонировать репозиторий
```
git clone git@github.com:avnosov3/YaTube.git
```
2. Перейти в папку с проектом и создать виртуальное окружение
```
cd YaTube
```
```
python3 -m venv env
python -m venv venv (Windows)
```
3. Активировать виртуальное окружение
```
source env/bin/activate
source venv/Scripts/activate (Windows)
```
4. Установить зависимости из файла requirements.txt
```
pip3 install -r requirements.txt
pip install -r requirements.txt (Windows)
```
5. Из папки yatube провести миграции
```
python3 manage.py migrate
python manage.py migrate (Windows)
```
6. Создать файл .env в папке yatube, где находится файл **settings.py**
```
SECRET_KEY=<указать секретный ключ>
DEBUG=True (если запуск в боевом режиме, то необходимо удалить пермеенную)

DB_ENGINE=django.db.backends.postgresql
DB_NAME=yatube
POSTGRES_USER=<Указать имя пользователя>
POSTGRES_PASSWORD=<Указать пароль>
DB_HOST=127.0.0.1
DB_PORT=<Указать порт для подключения к базе>
``` 
7. Запустить проека
```
python3 manage.py runserver
python manage.py runserver (Windows)
```
## Автор
[Артём Носов](https://github.com/avnosov3)