from django.conf import settings


def get_mysql_db_config():
    default = settings.DATABASES['default']
    return {
        'host': default.get('HOST'),
        'user': default.get('USER'),
        'password': default.get('PASSWORD'),
        'port': int(default.get('PORT', 3306)),
        'database': default.get('NAME'),
    }