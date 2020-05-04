import math
import re
import sys

import requests

from ShippingMethod.models import Drone, Robot
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils import *
from .scheduler import *
import datetime

from User.models import *
from Address.models import *
from Station.models import *
from Tracking.models import *
from OrderDetail.models import *


class OrderMapViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()

    def create(self, request):
        order_id = request.data.get('order_id', None)
        if order_id is None:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)

        order = OrderDetail.objects.get(id=order_id)

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

        data = requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
        if data['status'] != 'OK':
            return Response({"status": 400, "error": "Address has error"}, status=status.HTTP_400_BAD_REQUEST)

        if order.shipping_method == 'robot':
            first_part, second_part = parse_json(data)
        else:
            first_part = [data['routes'][0]['legs'][0]['start_location'], data['routes'][0]['legs'][0]['end_location']]
            second_part = [data['routes'][0]['legs'][1]['start_location'], data['routes'][0]['legs'][1]['end_location']]

        tracking_obj = order.tracking
        tracking_str = tracking_obj.street + '+' + tracking_obj.city + '+' + tracking_obj.state

        params_tracking = {
            'address': tracking_str,
            'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
        }

        tracking_data = requests.get(GEOCODE_BASE_URL, params_tracking).json()
        if tracking_data['status'] != 'OK':
            tracking_loc = {"lat": 0, "lng": 0}
        else:
            tracking_loc = tracking_data['results'][0]['geometry']['location']

        return Response({'response': {"first_part": first_part, "second_part": second_part, "tracking": tracking_loc},
                         'status': 200}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------
class SearchOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()

    def create(self, request):
        key = request.data.get('key', None)
        user_id = request.data.get('user_id', None)
        if key is None:
            return Response({'error': 'Missing search key', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        if user_id is None:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        sql = ""
        if key.isdigit():
            key = int(key)
            sql = 'SELECT O.id, category, status, lastname \
                     FROM \"OrderDetail_orderdetail\" AS O JOIN \"Address_address\" A2 ON O.to_address_id = A2.id\
                     WHERE O.user_id = {} \
                     AND O.id = {}'.format(user_id, key)
        else:
            sql = 'SELECT O.id, category, status, lastname \
                     FROM \"OrderDetail_orderdetail\" AS O JOIN \"Address_address\" A2 ON O.to_address_id = A2.id\
                     WHERE O.user_id = {} \
                     AND (LOWER( O.item_info ) LIKE \'%{}%\' OR LOWER( O.category ) LIKE \'%{}%\');'.format(user_id, key.lower(), key.lower())

        instance = executeSQL(sql)

        return Response({'response': instance, 'status': 200}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------
class OrderDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        order_id = request.data.get('order_id', None)
        if order_id is not None:
            # queryset = OrderDetail.objects.filter(user=user)
            sql = "SELECT * FROM \"OrderDetail_orderdetail\" O " \
                  "JOIN(SELECT id AS  from_id, firstname AS from_firstname, lastname AS from_lastname, " \
                  "street AS from_street, city AS from_city, state AS from_state, zipcode AS from_zipcode " \
                  "FROM \"Address_address\") A " \
                  "ON O.from_address_id = A.from_id " \
                  "JOIN(SELECT id AS to_id, firstname AS to_firstname, lastname AS to_lastname, " \
                  "street AS to_street, city AS to_city, state AS to_state, zipcode As to_zipcode " \
                  "FROM \"Address_address\") A2 " \
                  "ON O.to_address_id = A2.to_id " \
                  "WHERE O.id = {};".format(order_id)
            res = executeSQL(sql)
        else:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)
        if len(res) == 0:
            return Response({"status": 200, "response": {}}, status=status.HTTP_200_OK)
        return Response({"status": 200, "response": res[0]}, status=status.HTTP_200_OK)


# ----------------------------------------------------------------------------------------------------------------------
class OrderListViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('user_id', None)
        if user is None:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        sql = "SELECT O.id, category, status, lastname \
                FROM \"OrderDetail_orderdetail\" AS O JOIN \"Address_address\" A2 ON O.to_address_id = A2.id\
                WHERE O.user_id = {};".format(user)
        res = executeSQL(sql)
        return Response({"response": res, "status": 200}, status=status.HTTP_200_OK)


# ----------------------------------------------------------------------------------------------------------------
class PlaceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user_id = request.data.get('user_id', None)
        if user_id is None: return Response({"error": "Missing user id.", "status": 400},
                                            status=status.HTTP_400_BAD_REQUEST)
        order = self.save_orderdetail(request)

        current = datetime.datetime.now()
        schedule_time_first = current + datetime.timedelta(seconds=15)
        change_status_first(schedule_time_first, order)
        schedule_time_second = current + datetime.timedelta(seconds=40)
        change_status_second(schedule_time_second, order)
        return Response({"response": order.id, "status": 200}, status=status.HTTP_200_OK)

    def save_orderdetail(self, request):
        user_id = self.request.data.get('user_id', None)
        (from_address_id, to_address_id) = self.verify_address_id(request, user_id)
        station = request.data.get('station')
        shipping_method = request.data.get('shipping_method', None)
        amount = request.data.get('amount', None)
        category = request.data.get('packageCategory', None)
        capacity = request.data.get('packageWeight', 0.0)
        item_info = request.data.get('item_info', None)
        order_status = request.data.get('order_status', None)
        total_cost = request.data.get('fee', 0)
        pickup_time = request.data.get('MMDD') + ' ' + request.data.get('startSlot').split('-')[0]
        crt = datetime.datetime.now()
        pct = datetime.datetime.strptime(pickup_time, '%d-%m-%Y %H:%M')

        station_obj = Station.objects.get(id=station)
        tracking_obj = Tracking(street=station_obj.street, city=station_obj.city, state=station_obj.state,
                                zipcode=station_obj.zipcode)
        tracking_obj.save()
        
        po = OrderDetail(user=User.objects.get(id=user_id),
                         from_address=Address.objects.get(id=from_address_id),
                         to_address=Address.objects.get(id=to_address_id),
                         station=Station.objects.get(id=station),
                         tracking=tracking_obj,
                         item_info=item_info,
                         create_time=crt,
                         pickup_time=pct,
                         category=category,
                         capacity=capacity,
                         status=order_status,
                         shipping_method=shipping_method,
                         total_cost=total_cost,
                         feedback=0
                         )
        po.save()

        if shipping_method == 'drone':
            machine_list = StationDrone.objects.all().filter(status=0)[:amount]
            for drone_obj in machine_list:
                drone_obj.status = po.id
                drone_obj.save()
        if shipping_method == 'robot':
            machine_list = StationRobot.objects.all().filter(status=0)[:amount]
            for robot_obj in machine_list:
                robot_obj.status = po.id
                robot_obj.save()
        return po

    #verify address id if it exists
    def verify_address_id(self, request, user_id):
        faddr = request.data.get('fromAddress', None)
        taddr = request.data.get('toAddress', None)

        faddr_id = self.check_address_id(faddr, user_id)
        taddr_id = self.check_address_id(taddr, user_id)

        return faddr_id, taddr_id

    # If address id not exist, insert id
    def check_address_id(self, addr, user_id):
        if addr is None:
            return None
        try:
            if addr["addr_id"] != 0 : return addr["addr_id"]
            cur_id = self.get_address_id(user_id, addr["firstname"],
                                         addr["lastname"], addr["street"], addr["city"], addr["state"], addr["zipcode"])
            if cur_id is None:
                cur_id = self.insert_new_address(user_id, addr["firstname"], addr["lastname"], addr["street"],
                                                 addr["city"], addr["state"], addr["zipcode"])
            return cur_id
        except:
            print("Unable to get address Id")

    # check if address is already in DB
    def get_address_id(self, user_id, fname, lname, street, city, state, zipcode):

        addr = Address.objects.filter(firstname=fname, lastname=lname, street=street, city=city,
                                      state=state, zipcode=zipcode).values_list('id', flat=True)
        if not addr:
            return None
        else:
            addr_list = AddressList.objects.filter(user=user_id, address=addr[0])
            if not addr_list:
                addr_list = AddressList(user=User.objects.get(id=user_id), address=Address.objects.get(id=addr[0]))
                addr_list.save()
        return addr[0]

    # insert new address to DB
    def insert_new_address(self, user_id, fname, lname, street, city, state, zipcode):
        addr = Address(firstname=fname, lastname=lname, street=street, city=city, state=state, zipcode=zipcode)
        addr.save()
        addr_list = AddressList(user=User.objects.get(id=user_id), address=Address.objects.get(id=addr.id))
        addr_list.save()

        return addr.id


# ----------------------------------------------------------------------------------------------------------------
class OrderPlanViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        toAddress = request.data.get('toAddress')
        fromAddress = request.data.get('fromAddress')
        capacity = request.data.get('packageWeight')

        if toAddress is None or fromAddress is None:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)
        toAddressStreet = toAddress["street"]
        toAddressCity = toAddress["city"]
        toAddressState = toAddress["state"]
        fromAddressStreet = fromAddress["street"]
        fromAddressCity = fromAddress["city"]
        fromAddressState = fromAddress["state"]

        from_address_str = fromAddressStreet + '+' + fromAddressCity + '+' + fromAddressState
        to_address_Str = toAddressStreet + '+' + toAddressCity + '+' + toAddressState

        # time lowest
        # print(toAddressObj.state)
        # sql = "SELECT * FROM Station_station S " \
        #       "WHERE S.state = '{0}' ".format(toAddressObj.state)
        # instance = executeSQL(sql)

        instance = Station.objects.filter(state=fromAddressState)

        minPriceMethod = "drone"
        minPriceRating = 0.0
        minPrice = float('inf')
        minPriceStationId = -1
        minPriceTime = 0.0
        minPriceAmount = 0
        minDistanceRating = 0.0
        minTime = float('inf')
        minDistanceStationId = -1
        minDistancePrice = 0.0
        minDistanceMethod = "drone"
        minDistanceAmount = 0
        droneSpeed = 1.3
        robotSpeed = 0.8
        maxRatingStationId = -1
        maxRatingMethod = "drone"
        maxRating = 0.0
        maxRatingPrice = 0.0
        maxRatingTime = 0.0
        maxWeigh = -10000000000
        maxRatingAmount = 0

        for station in instance:
            state = station.state
            city = station.city
            street = station.street
            id = station.id
            rating = float(station.rating)
            station_str = street + '+' + city + '+' + state
            PARAMS = {
                'origin': station_str,
                'destination': to_address_Str,
                'waypoints': from_address_str,
                'mode': 'driving',
                'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
            }
            data = requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
            if data['status'] != 'OK':
                return Response({"status": 400, "error": "Address has error"}, status=status.HTTP_400_BAD_REQUEST)
            curDistance = re.findall(r"\d+\.?\d*", data['routes'][0]['legs'][0]['distance']['text'])
            availStationDrone = StationDrone.objects.filter(station=id)
            availDrone = getattr(availStationDrone.first(), 'drone')
            droneCapacity = float(getattr(availDrone, 'capacity'))
            dronePrice = float(getattr(availDrone, 'price'))
            availDroneNum = availStationDrone.filter(status=0).count()
            availStationRobot = StationRobot.objects.filter(station=id)
            availRobot = getattr(availStationRobot.first(), 'robot')
            robotCapacity = float(getattr(availRobot, 'capacity'))
            robotPrice = float(getattr(availRobot, 'price'))
            availRobotNum = availStationRobot.filter(status=0).count()
            if availDroneNum > math.ceil(capacity / droneCapacity):
                droneTotalPrice = float(math.ceil(capacity / droneCapacity) * dronePrice)
                if float(curDistance[0]) / droneSpeed < minTime:
                    minTime = float(curDistance[0]) / droneSpeed
                    minDistanceStationId = id
                    minDistanceRating = rating
                    minDistancePrice = droneTotalPrice
                    minDistanceMethod = "drone"
                    minDistanceAmount = math.ceil(capacity / droneCapacity)
                if droneTotalPrice < minPrice:
                    minPrice = droneTotalPrice
                    minPriceStationId = id
                    minPriceTime = float(curDistance[0]) / droneSpeed
                    minPriceMethod = "drone"
                    minPriceRating = rating
                    minPriceAmount = math.ceil(capacity / droneCapacity)
                droneWeigh = 0.4 * rating - 0.5 * float(curDistance[0]) / droneSpeed + 0.5 * droneTotalPrice
                if droneWeigh > maxWeigh:
                    maxWeigh = droneWeigh
                    maxRating = rating
                    maxRatingStationId = id
                    maxRatingMethod = "drone"
                    maxRatingTime = float(curDistance[0]) / droneSpeed
                    maxRatingPrice = droneTotalPrice
                    maxRatingAmount = math.ceil(capacity / droneCapacity)

            if availRobotNum > math.ceil(capacity / robotCapacity):
                robotTotalPrice = float(math.ceil(capacity / robotCapacity) * robotPrice)
                if float(curDistance[0]) / robotSpeed < minTime:
                    minTime = float(curDistance[0]) / robotSpeed
                    minDistanceStationId = id
                    minDistanceRating = rating
                    minDistancePrice = robotTotalPrice
                    minDistanceMethod = "robot"
                    minDistanceAmount = math.ceil(capacity / robotCapacity)
                if robotTotalPrice < minPrice:
                    minPrice = robotTotalPrice
                    minPriceStationId = id
                    minPriceMethod = "robot"
                    minPriceTime = float(curDistance[0]) / robotSpeed
                    minPriceRating = rating
                    minPriceAmount = math.ceil(capacity / robotCapacity)
                robotWeigh = 0.4 * rating - 0.5 * float(curDistance[0]) / robotSpeed + 0.5 * robotTotalPrice
                if robotWeigh > maxWeigh:
                    maxWeigh = robotWeigh
                    maxRatingStationId = id
                    maxRatingMethod = "robot"
                    maxRatingTime = float(curDistance[0]) / robotSpeed
                    maxRating = rating
                    maxRatingPrice = robotTotalPrice
                    maxRatingAmount = math.ceil(capacity / robotCapacity)

        if minPriceStationId == -1:
            return Response({"response": "There is no available plan", "status": 200}, status=status.HTTP_200_OK)

        return Response({"response": [{"type": 0,
                                       "station": maxRatingStationId,
                                       "fee": float(maxRatingPrice),
                                       "duration": math.ceil(maxRatingTime),
                                       "shipping_method": maxRatingMethod,
                                       "amount": maxRatingAmount,
                                       "rating": maxRating},
                                      {"type": 1,
                                       "station": minPriceStationId,
                                       "fee": float(minPrice),
                                       "duration": math.ceil(minPriceTime),
                                       "shipping_method": minPriceMethod,
                                       "amount": minPriceAmount,
                                       "rating": minPriceRating},
                                      {"type": 2,
                                       "station": minDistanceStationId,
                                       "fee": float(minDistancePrice),
                                       "duration": math.ceil(minTime),
                                       "shipping_method": minDistanceMethod,
                                       "amount": minDistanceAmount,
                                       "rating": minDistanceRating}],
                         "status": 200
                         }, status=status.HTTP_200_OK)

# ----------------------------------------------------------------------------------------------------------------
class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        order_id = request.data.get('order_id', None)
        feedback = request.data.get('feedback', None)
        if order_id is None:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)
        if feedback is None:
            return Response({"status": 400, "error": "Missing feedback."}, status=status.HTTP_400_BAD_REQUEST)
        order = OrderDetail.objects.get(id=order_id)
        feedback_old = order.feedback
        station_id = order.station_id
        order.feedback = feedback
        order.save()
        station = Station.objects.get(id=station_id)
        if feedback_old > 0:
            station.total_rating = station.total_rating - feedback_old
            station.rating_count = station.rating_count - 1
            station.save()
        count = station.rating_count
        prev_rating = station.total_rating
        sum = prev_rating + feedback
        count = count+1
        station.total_rating = sum
        station.rating_count = count
        station.rating = sum/count
        station.save()
        return Response({"response": "Feedback received", "status": 200}, status=status.HTTP_200_OK)
