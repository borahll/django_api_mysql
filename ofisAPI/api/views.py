# from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle

from api.models import Users
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import ItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# from rest_framework.views import APIView


# Create your views here.
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def apiOverView(request):
    user = request.user
    if request.objects.name != user:
        return Response({'response': 'You do not have permission'})
    users = Users.objects.all()
    serializer = ItemSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def addUser(request):
    serializer = ItemSerializer(data=request.data)
    data={}
    user = request.user
    if request.objects.name != user:
        return Response({'response': 'You do not have permission'})
    if serializer.is_valid():
        name = serializer.save()
        token = Token.objects.get(user=name).key
        data['token'] = token
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(self, request, pk):
    user = request.user
    if request.objects.name != user:
        return Response({'response': 'You do not have permission'})
    try:
        # Get the instance of the object to be deleted
        obj = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Delete the object
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def put(self, request, pk):
    user = request.user
    if request.objects.name != user:
        return Response({'response': 'You do not have permission'})
    try:
        instance = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPatchAPIView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = ItemSerializer


@api_view(['PATCH'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def patch(self, request, pk):
    user = request.user
    if request.objects.name != user:
        return Response({'response': 'You do not have permission'})
    try:
        instance = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
