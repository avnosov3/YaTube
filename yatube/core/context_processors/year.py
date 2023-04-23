import datetime as dt

today = dt.datetime.today()


def year(request):
    """Добавляет переменную с текущим годом."""
    request = today.year
    return {
        'year': request
    }
