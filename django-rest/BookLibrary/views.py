from django.shortcuts import render
from django.http import JsonResponse
from .models import Book

# Create your views here.
async def create_book(request):
    book = {
        "title": "Sample Book",
        "author": "John Doe",
        "published_date": "2023-01-01",
        "isbn": "1234567890123",
        "pages": 300,
        "cover_image": "http://example.com/cover.jpg"
    }
    Book.objects.create(**book)
    return JsonResponse(book)


async def get_books(request):
    books = Book.objects.all().values()
    return JsonResponse(list(books), safe=False)



async def get_book(request, book_id):
    book = Book.objects.filter(id=book_id).values().first()
    if book:
        return JsonResponse(book)
    return JsonResponse({"error": "Book not found"}, status=404)


async def update_book(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if book:
        # Update book details
        book.title = "Updated Title"
        book.author = "Updated Author"
        book.published_date = "2023-01-02"
        book.isbn = "1234567890124"
        book.pages = 350
        book.cover_image = "http://example.com/updated_cover.jpg"
        book.save()
        return JsonResponse({"message": "Book updated successfully"})
    return JsonResponse({"error": "Book not found"}, status=404)

async def delete_book(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if book:
        book.delete()
        return JsonResponse({"message": "Book deleted successfully"})
    return JsonResponse({"error": "Book not found"}, status=404)