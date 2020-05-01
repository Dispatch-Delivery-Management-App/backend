from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

from User.models import User
from OrderDetail.models import OrderDetail

class TrackingViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingSerializer

    def get_queryset(self):
        queryset = Tracking.objects.all()
        return queryset

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingSerializer
    def get_queryset(self):
        queryset = Tracking.objects.all()
        return queryset

    def create(self, request):
        user_id = request.data.get("user_id", None)
        if user_id is None:
            Response({"error": "No user id", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        send_notification(user_id)

        return Response({}, status=status.HTTP_200_OK)

def send_notification(user_id):
    # This registration token comes from the client FCM SDKs.
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_cred.json")
        firebase_admin.initialize_app(cred)

    user = User.objects.get(id=user_id)
    registration_token = user.token

    message = messaging.Message(
        notification=messaging.Notification(
            title='Order status has changed',
            body='This is a Notification Body for testing',
        ),
        token=registration_token,
    )
    # Send a message to the device corresponding to the provided registration token.

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    return response


class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingSerializer
    def get_queryset(self):
        queryset = Tracking.objects.all()
        return queryset

    def create(self, request):

        token = request.data.get('token', None)
        user_id = request.data.get('user_id', None)
        if token is None:
            return Response({'error': 'No token or user id', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = User.objects.get(id=user_id)
            user_obj.token = token
            user_obj.save()
            return Response({'response': {'Get your token'}, 'status': 200}, status=status.HTTP_200_OK)
        except:
            return Response({'error': {'User not found'}, 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
