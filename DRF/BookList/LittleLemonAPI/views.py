from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view, permission_classes, renderer_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from django.core.paginator import EmptyPage, Paginator
from rest_framework.throttling import AnonRateThrottle
from django.core.cache import cache

# Create your views here.
class MenuItemViews(generics.ListCreateAPIView):
    permission_classes = []
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    permission_classes = []
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        if category_name:
            items = items.filter(category__title = category_name)
        if to_price:
            print(f"Price Filter {to_price}")
            items = items.filter(price__lte = to_price)
        if search:
            items = items.filter(title__icontains = search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
                
        serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)

@api_view()
@permission_classes([AllowAny])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)


@api_view()
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialize_items = MenuItemSerializer(items, many=True)
    return Response({'data': serialize_items.data}, template_name='menu-items.html')


@api_view()
@permission_classes([AllowAny])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body>Welcome to Little Lemon</body></html>'
    return Response(data)

@api_view()
@permission_classes([AllowAny])
@renderer_classes([CSVRenderer])
def csv_render(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)

@api_view()
@permission_classes([AllowAny])
@renderer_classes([YAMLRenderer])
def yaml_render(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)


class SomeItems(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']
    
    
@api_view()
@permission_classes([IsAuthenticated])
def some_secret(request):
    return Response({"message": "some_secret"}, status.HTTP_200_OK)


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only Manager should see this"}, status.HTTP_200_OK)
    else:
        return Response({"message": "You are not authorized"}, status.HTTP_403_FORBIDDEN)

@api_view()
# @permission_classes([])
@throttle_classes([AnonRateThrottle])
def throttle_view(request):
    return Response({"message": "successfull"}, status.HTTP_200_OK)

@api_view()
def test_cache(request):
    cache.set('test_key', 'test_value', 60)
    value = cache.get('test_key')
    return Response({"cache_test": value})