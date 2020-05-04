from Station.models import *
from User.models import User
from Tracking.models import *

from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from .utils import *
import requests
import random

def change_status_first(schedule_time, order):
    #print(schedule_time)
    scheduler = BackgroundScheduler()
    scheduler.add_job(depart, 'date', run_date=schedule_time, args=[order])
    scheduler.start()

def change_status_second(schedule_time, order):
    #print(schedule_time)
    scheduler = BackgroundScheduler()
    scheduler.add_job(deliver, 'date', run_date=schedule_time, args=[order])
    scheduler.start()

def depart(order):
    #print("depart: ")

    if order.shipping_method == 'drone':
        # update tracking info
        update_drone_tracking(order)

        # give depart time
        order.depart_time = order.pickup_time -  datetime.timedelta(hours=1)
    if order.shipping_method == 'robot':
        # update tracking info
        update_robot_tracking(order)

        # give depart time
        order.depart_time = order.pickup_time -  datetime.timedelta(hours=2)
    order.status = 3
    order.save()
    #print("finish depart")

    # send notification
    send_notification(order.user_id, order.status, order.id)

def deliver(order):
    #print("deliver: ")
    if order.shipping_method == 'drone':
        # update tracking info
        tracking_obj = order.tracking
        to_address = order.to_address
        tracking_obj.street = to_address.street
        tracking_obj.city = to_address.city
        tracking_obj.state = to_address.state
        tracking_obj.zipcode = to_address.zipcode
        tracking_obj.save()

        # change drone status
        drones = StationDrone.objects.filter(status=order.id)
        for drone in drones:
            drone.status = 0
            drone.save()
        # give depart time
        order.complete_time = order.pickup_time +  datetime.timedelta(hours=1)
    if order.shipping_method == 'robot':
        # update tracking info
        tracking_obj = order.tracking
        to_address = order.to_address
        tracking_obj.street = to_address.street
        tracking_obj.city = to_address.city
        tracking_obj.state = to_address.state
        tracking_obj.zipcode = to_address.zipcode
        tracking_obj.save()

        # change robot status
        robots = StationRobot.objects.filter(status=order.id)
        for robot in robots:
            robot.status=0
            robot.save()
        # give depart time
        order.complete_time = order.pickup_time +  datetime.timedelta(hours=2)
    order.status = 4
    order.save()
    #print("finish deliver")

    # send notification
    send_notification(order.user_id, order.status, order.id)


def send_notification(user_id, order_status, order_id):
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_cred.json")
        firebase_admin.initialize_app(cred)

    user = User.objects.get(id=user_id)
    registration_token = user.token

    message_body = status_dict[order_status] + "order {} ".format(order_id)
    #print("message body: " + message_body)
    message = messaging.Message(
        notification=messaging.Notification(
            title='Order status has changed',
            body=message_body,
        ),
        token=registration_token,
    )
    response = messaging.send(message)


def update_drone_tracking(order):
    from_address_obj = order.from_address
    from_address_str = from_address_obj.street + '+' + from_address_obj.city + '+' + from_address_obj.state

    to_address_obj = order.to_address
    to_address_Str = to_address_obj.street + '+' + to_address_obj.city + '+' + to_address_obj.state

    station_obj = order.station
    station_str = station_obj.street + '+' + station_obj.city + '+' + station_obj.state

    PARAMS = {
        'origin': station_str,
        'destination': to_address_Str,
        'waypoints': from_address_str,
        'mode': 'driving',
        'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
    }

    geocode_data = requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
    first_part, _ = parse_json(geocode_data)
    lat1 = first_part[0]["lat"]
    lng1 = first_part[0]["lng"]

    lat2 = first_part[-1]["lat"]
    lng2 = first_part[-1]["lng"]
    a = lng1
    b = lat1
    c = lng2
    d = lat2
    e = random.uniform(a, c)
    tan = (c-a) / (d-b)
    f = (e-a) / tan + b
    res_lat = f
    res_lng = e
    latlng = str(res_lat) + ',' + str(res_lng)
    PARAMS_geocode = {
        'latlng': latlng,
        'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
    }

    tracking_data = requests.get(GEOCODE_BASE_URL, PARAMS_geocode).json()
    tracking_results = tracking_data["results"]

    formatted_address = ''
    for address_components in tracking_results:
        if 'street_address' in address_components["types"]:
            formatted_address = address_components["formatted_address"]
            break
    if formatted_address == '':
        formatted_address = tracking_results[0]['formatted_address']
    #print(formatted_address)
    street, city, state, zipcode = parse_formatted_address(formatted_address)

    tracking_obj = order.tracking
    tracking_obj.street = street
    tracking_obj.city = city
    tracking_obj.state = state
    tracking_obj.zipcode = zipcode
    tracking_obj.save()


def update_robot_tracking(order):
    from_address_obj = order.from_address
    from_address_str = from_address_obj.street + '+' + from_address_obj.city + '+' + from_address_obj.state

    to_address_obj = order.to_address
    to_address_Str = to_address_obj.street + '+' + to_address_obj.city + '+' + to_address_obj.state

    station_obj = order.station
    station_str = station_obj.street + '+' + station_obj.city + '+' + station_obj.state

    PARAMS = {
        'origin': station_str,
        'destination': to_address_Str,
        'waypoints': from_address_str,
        'mode': 'driving',
        'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
    }

    geocode_data = requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
    first_part, _ = parse_json(geocode_data)
    select_tracking = first_part[random.randint(0, len(first_part)-1)]

    latlng = str(select_tracking["lat"]) + ',' + str(select_tracking["lng"])
    PARAMS_geocode = {
        'latlng': latlng,
        'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
    }

    tracking_data = requests.get(GEOCODE_BASE_URL, PARAMS_geocode).json()
    tracking_results = tracking_data["results"]

    formatted_address = ''
    for address_components in tracking_results:
        if 'street_address' in address_components["types"]:
            formatted_address = address_components["formatted_address"]
            break
    if formatted_address == '':
        formatted_address = tracking_results[0]['formatted_address']

    #print(formatted_address)
    street, city, state, zipcode = parse_formatted_address(formatted_address)
    tracking_obj = order.tracking
    tracking_obj.street = street
    tracking_obj.city = city
    tracking_obj.state = state
    tracking_obj.zipcode = zipcode
    tracking_obj.save()


def parse_formatted_address(address):
    address_list = address.split(', ')

    street = address_list[-4] if len(address_list) == 4 else ", ".join(address_list[:-3])
    city = address_list[-3]
    state = address_list[-2].split(' ')[-2]
    zipcode = address_list[-2].split(' ')[-1]
    return street, city, state, zipcode
