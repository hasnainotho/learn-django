from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Menu
from .schema import MenuSerializer, MenuDetailSerializer

class MenuListCreateView(APIView):
    @extend_schema(request=MenuSerializer, responses=MenuSerializer)
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=MenuSerializer(many=True))
    def get(self, request):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
    
class MenuDetailView(APIView):
    @extend_schema(responses=MenuDetailSerializer)
    def get(self, request, menu_id):
        try:
            menu = Menu.objects.get(id=menu_id)
            serializer = MenuDetailSerializer(menu)
            return Response(serializer.data)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=MenuDetailSerializer, responses=MenuDetailSerializer)
    def put(self, request, menu_id):
        try:
            menu = Menu.objects.get(id=menu_id)
            serializer = MenuDetailSerializer(menu, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, menu_id):
        try:
            menu = Menu.objects.get(id=menu_id)
            menu.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)