from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q

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


class SearchResultsView(ListView):
    model = Book
    template_name = 'layout/main.html'
    context_object_name = 'books'
    ordering = ['title']
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(book_description__icontains=query)
            | Q(author__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
