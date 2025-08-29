from django.urls import path, include
import BookListAPI.views as views
from rest_framework.routers import DefaultRouter


# Router for protected endpoints (authentication required)
protected_router = DefaultRouter(trailing_slash=True)
protected_router.register('books', views.BookView, basename='protected-books')

# Router for public endpoints (read-only for anonymous, full access for authenticated)
public_router = DefaultRouter(trailing_slash=True)
public_router.register('public-books', views.PublicBookView, basename='public-books')

urlpatterns = [
    # Public endpoint - no authentication required
    path('public/', views.public_books, name='public-books-list'),
    
    # Admin only endpoint
    path('admin/books/', views.AdminBookView.as_view(), name='admin-books'),
    
    # Protected routes - authentication required
    path('protected/', include(protected_router.urls)),
    
    # Public routes - mixed permissions
    path('', include(public_router.urls)),
]