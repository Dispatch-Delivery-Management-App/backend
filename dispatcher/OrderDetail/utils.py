from django.db import connection

status_dict = {
    1: "Draft",
    2: "Not start",
    3: "Depart to pick up ",
    4: "Complete "
}

GOOGLEMAP_BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json'
GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

def executeSQL(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def parse_json(data):

    legs = data['routes'][0]['legs']
    first_dict = []
    second_dict = []

    for j in range(len(legs)):
        leg_obj = legs[j]
        steps = leg_obj['steps']
        for i in range(len(steps)):
            step = steps[i]
            if i == 0 and j == 0:
                first_dict.append(step['start_location'])
            if i == 0 and j == 1:
                second_dict.append(step['start_location'])
            if j == 0:
                first_dict.append(step['end_location'])
            if j == 1:
                second_dict.append(step['end_location'])
    return first_dict, second_dict
