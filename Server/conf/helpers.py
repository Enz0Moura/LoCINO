from datetime import datetime


def format_data(data: datetime) -> str:
    return data.strftime('%d.%m.%Y %H:%M')