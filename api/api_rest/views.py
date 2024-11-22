from csv import excel

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer
import json

@api_view(['GET'])
def get_users(request):

     if request.method == 'GET':
         users = User.objects.all()

         serializer = UserSerializer(users, many=True)
         return Response(serializer.data)

     return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_by_caique(request, nick):

    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':

        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):
    # ACESSOS

    if request.method == 'GET':

        try:
            if request.GET['user']:  # Check if there is a get parameter called 'user' (/?user=xxxx&...)

                user_nickname = request.GET['user']  # Find get parameter

                try:
                    user = User.objects.get(pk=user_nickname)  # Get the object in database
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = UserSerializer(user)  # Serialize the object data into json
                return Response(serializer.data)  # Return the serialized data

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#criando dados
    if request.method =='POST':
        new_user = request.data
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)