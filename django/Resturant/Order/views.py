# from django.shortcuts import render
# from django.http import JsonResponse
# from django.db import models
# from .models import Order
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from .schema import OrderSerializer

# # Create your views here.
# async def create_order(APIView):
#     if request.method == 'POST':
#         serializer = OrderSerializer(data=request.POST)
#         if serializer.is_valid():
#             order = serializer.save()
#             return JsonResponse({'message': 'Order created successfully', 'order_id': order.id}, status=201)
#         return JsonResponse({'error': 'Invalid data'}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# @csrf_exempt
# async def create_order(request):
#     if request.method == 'POST':
#         serializer = OrderSerializer(data=request.POST)
#         if serializer.is_valid():
#             order = serializer.save()
#             return JsonResponse({'message': 'Order created successfully', 'order_id': order.id}, status=201)
#         return JsonResponse({'error': 'Invalid data'}, status=400)
#     elif request.method == 'GET':
#         customer_name = request.GET.get('customer_name')
#         total_amount = request.GET.get('total_amount')  # Assuming total_amount is a string that can be converted to Decimal
#         if not customer_name or not total_amount:
#             return JsonResponse({'error': 'Missing required fields'}, status=400)
#         order = Order.objects.create(customer_name=customer_name, total_amount=total_amount)
#         return JsonResponse({'message': 'Order created successfully', 'order_id': order.id}, status=201)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# async def get_order(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         return JsonResponse({
#             'id': order.id,
#             'customer_name': order.customer_name,
#             'order_date': order.order_date.isoformat(),
#             'total_amount': str(order.total_amount)
#         })
#     except Order.DoesNotExist:
#         return JsonResponse({'error': 'Order not found'}, status=404)
    
    
# async def list_orders(request):
#     orders = Order.objects.all().values('id', 'customer_name', 'order_date', 'total_amount')
#     return JsonResponse(list(orders), safe=False, status=200)

# async def delete_order(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         order.delete()
#         return JsonResponse({'message': 'Order deleted successfully'}, status=204)
#     except Order.DoesNotExist:
#         return JsonResponse({'error': 'Order not found'}, status=404)
    
# async def update_order(request, order_id):
#     if request.method == 'PUT':
#         try:
#             order = Order.objects.get(id=order_id)
#             customer_name = request.PUT.get('customer_name', order.customer_name)
#             total_amount = request.PUT.get('total_amount', order.total_amount)
            
#             order.customer_name = customer_name
#             order.total_amount = total_amount
#             order.save()
            
#             return JsonResponse({'message': 'Order updated successfully'}, status=200)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# async def order_summary(request):
#     total_orders = Order.objects.count()
#     total_amount = Order.objects.aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0

#     return JsonResponse({
#         'total_orders': total_orders,
#         'total_amount': str(total_amount)
#     }, status=200)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Order
from .schema import OrderSerializer, OrderDetailSerializer

class OrderListCreateView(APIView):
    @extend_schema(request=OrderSerializer, responses=OrderSerializer)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=OrderSerializer(many=True))
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class OrderDetailView(APIView):
    @extend_schema(responses=OrderDetailSerializer)
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=OrderDetailSerializer, responses=OrderDetailSerializer)
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderDetailSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
