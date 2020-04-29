from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def create(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None:
            return Response({"error":"No user name.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return Response({"error":"No password.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User name not found.', 'status': 404}, status=status.HTTP_404_NOT_FOUND)
        else:
            if user.password == password:
                return Response({"response": {"id": user.id, "username": user.username, "email":user.email, "password":user.password, "firstname":user.firstname, "lastname":user.lastname}, "status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password.', 'status':401}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def create(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)
        firstname = request.data.get('firstname', None)
        lastname = request.data.get('lastname', None)

        if username is None:
            return Response({"error":"No user name.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return Response({"error":"No password.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            instance = User(username=username, type=1, password=password, email=email, firstname=firstname, lastname=lastname)
            instance.save()
            return Response({"response": {"id": instance.id, "username": instance.username, "email":instance.email, "password":instance.password, "firstname":instance.firstname, "lastname":instance.lastname}, "status": 201}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"User name already exists.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
