from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import SerializerMenu
from .serializer import SerializerMenuItemsSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all(request):
    items = SerializerMenu.objects.all()
    serialized_item = SerializerMenuItemsSerializer(items, many=True)
    return Response(serialized_item.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_item(request):
    serializer = SerializerMenuItemsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_item(request, pk):
    item = get_object_or_404(SerializerMenu, pk=pk)
    serialized_item = SerializerMenuItemsSerializer(item)
    return Response(serialized_item.data)
