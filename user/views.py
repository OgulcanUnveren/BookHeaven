from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from user.permission import IsAdminUser, IsLoggedInUserOrSuperAdmin, IsAdminOrAnonymousUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
# from user.permission import HasGroupPermission
#
# permission importing from my_permission fro APIView
# from user.my_permission import HasGroupPermission as APIViewPermission
#
from user.models import User
from user.serializers import UserSerializer
from rest_framework.filters import BaseFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    # permission_classes = (HasGroupPermission, )
    # permission_groups = {
    #     'create': ['admin'],
    #     'list': ['admin', 'anonymous'],
    #     'retrieve': ['admin', 'anonymous'],
    #     'update': ['admin', 'anonymous'],
    #     'destroy': ['admin']
    # }

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAdminOrAnonymousUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrSuperAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsLoggedInUserOrSuperAdmin]
        return [permission() for permission in permission_classes]



@api_view(['GET']) # Add this
@permission_classes([IsAuthenticated]) # Maybe add this too
def getusers(request):
    products = User.objects.all()
    serializer = UserSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['POST']) # Add this
@permission_classes([IsAdminUser]) # Maybe add this too
def deluser(request):
    id = request.POST.get('id')
    products = User.objects.filter(id=id)
    if products is not None:
        User.objects.filter(id=id).delete()
        data = {
            '200':'success'
        }
        return Response(data)

# view for registering users
# APIView defined for UserView
class UserView(APIView):
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAdminOrAnonymousUser]
     

     def get(self, request):
        products = User.objects.all()
        serializer = UserSerializer(products, many=True)
        return Response(serializer.data)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'group': openapi.Schema(type=openapi.TYPE_INTEGER),
    }
))
@api_view(['POST'])
def  Register(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)