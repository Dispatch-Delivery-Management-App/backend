from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

global_token = ''

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
        global global_token
        # This registration token comes from the client FCM SDKs.
        cred = credentials.Certificate("dispatcher-275400-firebase-adminsdk-kzph2-2aee0b9347.json")
        firebase_admin.initialize_app(cred)

        registration_token = 'AAAAvmDabd0:APA91bHQfv-SvhVy4O6hnp8x3arVfcmZNOCIxWvWcWKRjMMUXcajkruuPbHhDAhbDuXC5VJarx4N426Ik2kDsh8PbqGjAKCf7AZ8-hBLGUhIahXrgK4vegSOrnVV0g5a8sMDja670YE5'
        #registration_token = 'AIzaSyB9Porku8jH1c7fzaLtpI2Pu5IdWRUuKXw'
        # See documentation on defining a message payload.
        message = messaging.Message(
            data={
                'score': '850',
                'time': '2:45',
            },
            token=registration_token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)

        return Response({}, status=status.HTTP_200_OK)

class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingSerializer
    def get_queryset(self):
        queryset = Tracking.objects.all()
        return queryset

    def create(self, request):

        token = request.data.get('token', None)
        if token is None:
            return Response({'error': 'No token provided', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        global global_token
        print(global_token)
        global_token = token
        print(global_token)
        return Response({'response': {'Get your token'}, 'status': 200}, status=status.HTTP_200_OK)
