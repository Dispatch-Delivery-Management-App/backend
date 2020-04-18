from django.db import connection

status_dict = {
    "draft": 1,
    "incomplete": 2,
    "complete": 3
}


def executeSQL(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        #res = cursor.fetchall()
        #return(res)
