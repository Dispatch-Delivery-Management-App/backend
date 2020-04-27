import re
import sys

from ShippingMethod.models import Drone, Robot
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils import *
import datetime
import requests

from User.models import User
from Address.models import Address
from Address.models import AddressList
from Station.models import Station
from Tracking.models import Tracking
from OrderDetail.models import OrderDetail

class OrderMapViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()

    def create(self, request):
        order_id = request.data.get('order_id', None)
        if order_id is  None:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)

        order = OrderDetail.objects.get(id=order_id)

        from_address_obj = order.from_address
        from_address_str = from_address_obj.street+'+'+from_address_obj.city+'+'+from_address_obj.state

        to_address_obj = order.to_address
        to_address_Str = to_address_obj.street+'+'+to_address_obj.city+'+'+to_address_obj.state

        station_obj = order.station
        station_str = station_obj.street+'+'+station_obj.city+'+'+station_obj.state

        PARAMS = {
            'origin': station_str,
            'destination': to_address_Str,
            'waypoints': from_address_str,
            'mode': 'driving',
            'key':'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
            }

        data= requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
        print(data)
        if data['status'] != 'OK':
            return Response({"status": 400, "error": "Address has error"}, status=status.HTTP_400_BAD_REQUEST)

        if order.shipping_method == 'robot':
            first_part, second_part = parse_json(data)
        else:
            first_part = [data['routes'][0]['legs'][0]['start_location'], data['routes'][0]['legs'][0]['end_location']]
            second_part = [data['routes'][0]['legs'][1]['start_location'], data['routes'][0]['legs'][1]['end_location']]

        return Response({'response': {"first_part": first_part,"second_part": second_part}, 'status':200}, status=status.HTTP_200_OK)


class SearchOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()

    def create(self, request):
        key = request.data.get('key', None)
        user_id = request.data.get('user_id', None)
        if key is None:
            return Response({'error': 'Missing search key', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        if user_id is None:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        sql = 'SELECT * FROM dispatcher.OrderDetail_orderdetail where user_id = {} \
                AND (id = \"{}\"\
                OR LOWER( item_info ) LIKE \"%{}%\");'.format(user_id, key, key)
        instance = executeSQL(sql)
        return Response({'response': instance, 'status':200}, status=status.HTTP_200_OK)

class OrderDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        order_id = request.data.get('order_id', None)
        if order_id is not None:
            # queryset = OrderDetail.objects.filter(user=user)
            sql = "SELECT * FROM OrderDetail_orderdetail O "\
                  "JOIN(SELECT id AS  from_id, firstname AS from_firstname, lastname AS from_lastname, " \
                  "street AS from_street, city AS from_city, state AS from_state, zipcode AS from_zipcode "\
                  "FROM Address_address) A "\
                  "ON O.from_address_id = A.from_id "\
                  "JOIN(SELECT id AS to_id, firstname AS to_firstname, lastname AS to_lastname, " \
                  "street AS to_street, city AS to_city, state AS to_state, zipcode As to_zipcode " \
                  "FROM Address_address) A2 " \
                  "ON O.to_address_id = A2.to_id " \
                  "WHERE O.id = {};".format(order_id)
            res = executeSQL(sql)
        else:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)
        if len(res) == 0:
            return Response({"status": 200, "response": {}}, status=status.HTTP_200_OK)
        return Response({"status": 200, "response": res[0]}, status=status.HTTP_200_OK)

class OrderListViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('user_id', None)
        if user is None:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        res = {}
        for order_status in range(1,5):
            sql = "SELECT OrderDetail_orderdetail.id, category, status, lastname \
            FROM OrderDetail_orderdetail JOIN Address_address A2 ON OrderDetail_orderdetail.to_address_id = A2.id\
            WHERE OrderDetail_orderdetail.user_id = {} and OrderDetail_orderdetail.status = {};".format(user, order_status)
            sql_res = executeSQL(sql)
            res[order_status] = sql_res
        return Response({"response": res, "status": 200}, status=status.HTTP_200_OK)


class PlaceOrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self,request):
        print("in create")
        user_id = request.data.get('user_id', None)
        if user_id is None: return Response({"error": "Missing user id.", "status": 400},
                                            status=status.HTTP_400_BAD_REQUEST)
        #try;;
        self.save_orderdetail(request)
        return Response({"response": "Should be plan list here","status": 200}, status=status.HTTP_200_OK)

    def save_orderdetail(self,request):
        user_id = self.request.data.get('user_id', None)
        (from_address_id, to_address_id)= self.verify_address_id(request, user_id)
        print(from_address_id,to_address_id)
        station= request.data.get('station')
        tracking= request.data.get('tracking')
        category = request.data.get('packageCategory', None)
        capacity = request.data.get('packageWeight', 0.0)
        item_info = request.data.get('item_info', None)
        pickup_time = request.data.get('MMDD') + ' ' + request.data.get('startSlot').split('-')[0]
        print(pickup_time)
        crt = datetime.datetime.now()
        pct = datetime.datetime.strptime(pickup_time, '%d-%m-%Y %H:%M')

        print(pickup_time)
        print(pct)

        po = OrderDetail(user=User.objects.get(id=user_id),
                         from_address=Address.objects.get(id=from_address_id),
                         to_address=Address.objects.get(id=to_address_id),
                         station=Station.objects.get(id=station),
                         tracking=Tracking.objects.get(id=tracking),
                         item_info=item_info,
                         create_time=crt,
                         pickup_time=pct,
                         category=category,
                         capacity=capacity #,status=status
                         )
        po.save()


    def verify_address_id(self, request, user_id):
        print("In verify_address_id")
        faddr = request.data.get('fromAddress', None)
        taddr = request.data.get('toAddress', None)

        faddr_id = self.check_address_id(faddr, user_id)
        taddr_id = self.check_address_id(taddr, user_id)
        print("in verify_address_id",faddr_id, taddr_id)
        return faddr_id, taddr_id

    #If address id not exist, insert id
    def check_address_id(self, addr, user_id):
        print("check_address_id")
        if addr is None:
            return None
        try:
            if "addr_id" in addr: return addr["addr_id"]
            cur_id = self.get_address_id(user_id, addr["firstname"],
                                    addr["lastname"], addr["street"], addr["city"], addr["state"], addr["zipcode"])
            if cur_id is None:
                cur_id = self.insert_new_address(user_id, addr["firstname"],
                                addr["lastname"], addr["street"], addr["city"], addr["state"], addr["zipcode"])
            return cur_id
        except:
            print("Unable to get address Id")

    #check if address is already in DB
    def get_address_id(self, user_id, fname, lname, street, city, state, zipcode):

        addr = Address.objects.filter(firstname=fname, lastname=lname, street=street, city=city,
                                      state=state,zipcode=zipcode).values_list('id', flat=True)
        if not addr:
            return None
        else:
            addr_list = AddressList.objects.filter(user=user_id, address=addr[0])
            if not addr_list:
                addr_list = AddressList(user=User.objects.get(id=user_id), address=Address.objects.get(id=addr[0]))
                addr_list.save()
        return addr[0]

    #insert new address to DB
    def insert_new_address(self,user_id, fname, lname, street, city, state, zipcode):
        print("in insert_new_address")
        addr = Address(firstname=fname, lastname=lname, street=street, city=city,state=state,zipcode=zipcode)
        addr.save()
        addr_list = AddressList(user=User.objects.get(id=user_id), address=Address.objects.get(id=addr.id))
        addr_list.save()

        print("save addrlist",addr.id)
        return addr.id
    
class OrderPlanViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        toAddress = request.data.get('to_address')
        fromAddress = request.data.get('from_address')
        capacity = request.data.get('capacity')

        if toAddress is None or fromAddress is None:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)

        toAddressObj = Address.objects.get(id=toAddress)

        fromAddressObj = Address.objects.get(id=fromAddress)
        from_address_str = fromAddressObj.street + '+' + fromAddressObj.city + '+' + fromAddressObj.state
        to_address_Str = toAddressObj.street + '+' + toAddressObj.city + '+' + toAddressObj.state

        #time lowest
        print(toAddressObj.state)
        sql = "SELECT * FROM dispatcher.Station_station S " \
              "WHERE S.state = '{0}' ".format(toAddressObj.state)
        instance = executeSQL(sql)
        print(instance)
        globalDistance = 1000000.0
        globalStationId = -1
        for station in instance:
            state = station.get('state')
            city = station.get('city')
            street = station.get('street')
            id = station.get('id')
            station_str = street + '+' + city + '+' + state
            PARAMS = {
                'origin' : station_str,
                'destination' : to_address_Str,
                'waypoints' : from_address_str,
                'mode' : 'driving',
                'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
            }
            data = requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
            if data['status'] != 'OK':
                return Response({"status": 400, "error": "Address has error"}, status=status.HTTP_400_BAD_REQUEST)
            curDistance = re.findall(r"\d+\.?\d*",data['routes'][0]['legs'][0]['distance']['text'])
            if float(curDistance[0]) < globalDistance:
                globalDistance = float(curDistance[0])
                globalStationId = id
        fastTime = int(globalDistance / 1.5)
        fastMethod = "Drone"

        #price lowest

        lowestPriceMethod = "Drone"
        droneObj = Drone.objects.first()
        droneCapacity = float(getattr(droneObj, 'capacity'))
        dronePrice = int(getattr(droneObj, 'price'))
        robotObj = Robot.objects.first()
        robotCapacity = float(getattr(robotObj, 'capacity'))
        robotPrice = int(getattr(robotObj, 'price'))
        rating = Station.objects.all()
        ratingList = rating.values_list('rating', flat=True)
        totalRating = float(ratingList[0])
        cheapCost = sys.maxsize
        fastCost = float(capacity / droneCapacity) * dronePrice
        fastAmount = int((capacity / droneCapacity) + 1)
        CheapAmount = 0
        if (capacity / droneCapacity + 1) * dronePrice < (capacity / robotCapacity + 1) * robotPrice:
            lowestPriceMethod = "Drone"
            cheapCost = (capacity / droneCapacity + 1) * dronePrice
            cheapAmount = int(capacity / droneCapacity + 1)
            cheapTime = fastTime + 10
        else:
            lowestPriceMethod = "Robot"
            cheapCost = (capacity / robotCapacity + 1) * robotPrice
            cheapAmount = int(capacity / robotCapacity + 1)
            cheapTime = fastTime + 10
        return Response([{"type": 2,
                          "station": globalStationId,
                          "fee": fastCost,
                          "duration": fastTime,
                          "shipping_method": fastMethod,
                          "amount": fastAmount,
                          "rating": totalRating},
                          {"type":1,
                           "station": globalStationId,
                           "fee":cheapCost,
                           "duration": cheapTime,
                           "shipping_method": lowestPriceMethod,
                           "amount": cheapAmount,
                           "rating":totalRating}])
