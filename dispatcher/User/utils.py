from django.db import connection

def executeSQL(sql):
    with connection.cursor() as cursor:
        res = cursor.execute(sql)
        return(res)
