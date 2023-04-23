import datetime as dt

today = dt.datetime.today()


def year(request):
    """Добавляет переменную с текущим годом."""
    return {'year': dt.datetime.today().year}
