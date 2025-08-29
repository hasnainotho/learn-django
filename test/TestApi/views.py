from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from . import serializers
from . import throttles
from . import models
from rest_framework import status
import logging

# Create your views here.

logger = logging.getLogger(__name__)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_view(request):
    logger.info(f"Request from IP: {request.META.get('REMOTE_ADDR')}, user: {request.user}, method: {request.method}")
    if hasattr(request, 'throttled') and request.throttled:
        logger.warning("Request was throttled!")
    return Response({"message": "Throttle Response"}, status.HTTP_200_OK)


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def user_throttle(request):
    logger.info(f"Request from IP: {request.META.get('REMOTE_ADDR')}, user: {request.user}, method: {request.method}")
    if hasattr(request, 'throttled') and request.throttled:
        logger.warning("Request was throttled!")
    return Response({"message": "User Throttle Response"}, status.HTTP_200_OK)


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([throttles.TenMinutesThrottle])
def ten_throttle(request):
    logger.info(f"Request from IP: {request.META.get('REMOTE_ADDR')}, user: {request.user}, method: {request.method}")
    if hasattr(request, 'throttled') and request.throttled:
        logger.warning("Request was throttled!")
    return Response({"message": "User Ten Throttle Response"}, status.HTTP_200_OK)


class TestViewSet(ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    queryset = models.TestModel.objects.all()
    serializer_class = serializers.TestSerializer
    
    # def get_throttle(self):
    #     if self.action == "create":
    #         throttle_classes = [UserRateThrottle]
    #     else:
    #         throttle_classes = [AnonRateThrottle]
    
    
class TestDetailViewSet(RetrieveUpdateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = models.TestModel.objects.all()
    serializer_class = serializers.TestSerializer
    
    
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "some secret"}, status.HTTP_200_OK)



@api_view(["POST", "DELETE"])
@permission_classes([IsAdminUser])
def manager_view(request):
    username = request.data["username"]
    if username:
        user = get_object_or_404(User, username=username)
        manager = Group.objects.get(name="Manager")
        if request.method == "POST":
            manager.user_set.add(user)
        if request.method == "DELETE":
            manager.user_set.remove(user)
        return Response({"message": "ok"}, status.HTTP_200_OK)
    
    return Response({"message": "Missing username"}, status.HTTP_400_BAD_REQUEST)