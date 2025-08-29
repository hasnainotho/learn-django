from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.
class MenuView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        item = request.GET.get('item')
        if item:
            return Response({'message': f'Menu Listing Item {item}'}, status.HTTP_200_OK)
            
        return Response({'message': f'Menu Listing Item'}, status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'message': f"Menu Item {request.data.get('title')}"}, status.HTTP_201_CREATED)
    
    
class Menu(APIView):
    permission_classes = []
    def get(self, request, pk):
        return Response({'message': f"The Item with Id {pk}"}, status.HTTP_200_OK)