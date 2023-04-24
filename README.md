# [YaTube](https://budiroga.pythonanywhere.com/)
[YaTube](https://budiroga.pythonanywhere.com/) - социальная сеть, в которой реализована возможность публикации и комментирования постов,
подписки на авторов. В проекте использована пагинация и кеширование страниц. Написаны
тесты для проверки реализованных функций сайта и подключен django-debug-toolbar. Дополнительно разработан REST [API](https://budiroga.pythonanywhere.com/api/v1/redoc/) для сервиса [(документация API)](https://budiroga.pythonanywhere.com/api/v1/redoc/).

## Техно-стек
* [![Python](https://img.shields.io/badge/Python-3.7.9-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
* [![Django](https://img.shields.io/badge/Django-2.2.16-blue?style=flat-square&logo=Django&logoColor=092E20&labelColor=d0d0d0)](https://www.djangoproject.com/)
* [![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.12.4-blue?style=flat-square&logo=Django&logoColor=a30000&labelColor=d0d0d0)](https://www.django-rest-framework.org/)
* [![Simple JWT](https://img.shields.io/badge/Simple%20JWT%20-4.7.2-blue?style=flat-square&logo=github&logoColor=4285F4&labelColor=d0d0d0)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [![Djoser](https://img.shields.io/badge/Djoser-2.1.0-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://djoser.readthedocs.io/)
* [![Django Debug Toolbar](https://img.shields.io/badge/Django%20Debug%20Toolbar-3.2.4-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://django-debug-toolbar.readthedocs.io/)
* [![Pillow](https://img.shields.io/badge/Pillow-8.3.1-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://python-pillow.org/)
* [![Sorl-thumbnail](https://img.shields.io/badge/Sorl-thumbnail-12.7.0-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://sorl-thumbnail.readthedocs.io/)

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
6. Запустить проект
```
python3 manage.py runserver
python manage.py runserver (Windows)
```
## Автор
[Артём Носов](https://github.com/avnosov3)