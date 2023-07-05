# [YaTube](https://budiroga.pythonanywhere.com/)

<details><summary>Russian language</summary>  
  
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
5. Создать файл .env в папке yatube, в которой находится файл **settings.py**
```
SECRET_KEY=<указать секретный ключ>
DEBUG=True (если запуск в боевом режиме, то необходимо удалить переменную)

DB_ENGINE=<Указать движок БД>
DB_NAME=<Указать название БД>
POSTGRES_USER=<Указать имя пользователя>
POSTGRES_PASSWORD=<Указать пароль>
DB_HOST=<Указать хост>
DB_PORT=<Указать порт для подключения к базе>
``` 
6. Перейти на уровень выше и провести миграции
```
cd ..
```
```
python3 manage.py migrate
python manage.py migrate (Windows)
```
7. Создать супер пользователя
```
python3 manage.py createsuperuser
python manage.py createsuperuser (Windows)
```
8. Запустить проект
```
python3 manage.py runserver
python manage.py runserver (Windows)
```

## Автор
[Артём Носов](https://github.com/avnosov3)
</details>

<details><summary>English language</summary>  
  
[YaTube](https://budiroga.pythonanywhere.com/) - a social network that implements the ability to publish and comment on posts,
Author Subscriptions. The project uses pagination and page caching. Written
tests to check the implemented functions of the site and the django-debug-toolbar is included. Additionally developed REST [API](https://budiroga.pythonanywhere.com/api/v1/redoc/) for service [(API documentation)](https://budiroga.pythonanywhere.com/api/v1/redoc/) .

## Stack
* python 3.7.9
* django 2.2.16
* drf 3.12.4
* drf-simlejwt 4.7.2
* djoser 2.1.0
* django-debug-toolbar 3.2.4
* pillow 8.3.1
* sorl-thumbnail 12.7.0
* postgres 13.0

## Launch of the project
1. Clone repository
```
git clone git@github.com:avnosov3/YaTube.git
```
2. Go to the project folder and create a virtual environment
```
cd YaTube
```
```
python3 -m venv env
python -m venv venv (Windows)
```
3. Activate a virtual environment
```
source env/bin/activate
source venv/Scripts/activate (Windows)
```
4. Install dependencies from requirements.txt file
```
pip3 install -r requirements.txt
pip install -r requirements.txt (Windows)
```
5. Create .env file in yatube folder where **settings.py** file is located
```
SECRET_KEY=<specify secret key>
DEBUG=True (if the launch is in prod mode, then you need to delete the variable)

DB_ENGINE=<Specify database engine>
DB_NAME=<Specify database name>
POSTGRES_USER=<Specify username>
POSTGRES_PASSWORD=<Specify password>
DB_HOST=<Specify host>
DB_PORT=<Specify the port to connect to the base>
``` 
6. Go up a level and run migrations
```
cd ..
```
```
python3 manage.py migrate
python manage.py migrate (Windows)
```
7. Create super user
```
python3 manage.py createsuperuser
python manage.py createsuperuser (Windows)
```
8. Start project
```
python3 manage.py runserver
python manage.py runserver (Windows)
```

## Author
[Artem Nosov](https://github.com/avnosov3)
</details>
