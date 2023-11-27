from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'layout/index.html')


def main(request):
    books = Book.objects.all()
    books_per_page = 8  # You can adjust this number based on your preference

    paginator = Paginator(books, books_per_page)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:

        books = paginator.page(1)
    except EmptyPage:

        books = paginator.page(paginator.num_pages)

    return render(request, 'layout/main.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'layout/book_detail.html', {'book': book})