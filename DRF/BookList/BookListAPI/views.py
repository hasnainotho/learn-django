from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.routers import SimpleRouter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import BookList
from rest_framework import serializers


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookList
        fields = ['id', 'title', 'author', 'published_date', 'isbn']


# Public API - No authentication required
@api_view(['GET'])
@permission_classes([AllowAny])
def public_books(request):
    """
    Public endpoint - anyone can access
    """
    books = BookList.objects.all()
    serializer = BookListSerializer(books, many=True)
    return Response({
        'message': 'Public book list',
        'books': serializer.data
    }, status=status.HTTP_200_OK)


# Protected API - Authentication required
class BookView(viewsets.ModelViewSet):
    """
    Protected endpoints - authentication required for all operations
    """
    queryset = BookList.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'message': f'Books list for authenticated user: {request.user.username}',
            'books': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Book created by: {request.user.username}',
                'book': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mixed permissions - Read for all, Write for authenticated
class PublicBookView(viewsets.ModelViewSet):
    """
    Mixed permissions: 
    - GET (list/retrieve) - Anyone can access
    - POST/PUT/PATCH/DELETE - Authentication required
    """
    queryset = BookList.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        user_info = f" (User: {request.user.username})" if request.user.is_authenticated else " (Anonymous user)"
        return Response({
            'message': f'Public book list{user_info}',
            'books': serializer.data
        }, status=status.HTTP_200_OK)


# Admin only operations
class AdminBookView(APIView):
    """
    Admin only endpoints - requires staff/superuser permissions
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"User: {request.user.is_staff}")
        if not request.user.is_staff:
            return Response({
                'error': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        books = BookList.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response({
            'message': f'Admin view - accessed by: {request.user.username}',
            'books': serializer.data,
            'total_books': books.count()
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.is_superuser:
            return Response({
                'error': 'Superuser access required to delete all books'
            }, status=status.HTTP_403_FORBIDDEN)
        
        count = BookList.objects.count()
        BookList.objects.all().delete()
        return Response({
            'message': f'All {count} books deleted by superuser: {request.user.username}'
        }, status=status.HTTP_200_OK)


