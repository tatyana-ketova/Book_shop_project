from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q

def home(request):
    return render(request, 'layout/index.html')


def main(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')

    if selected_category:
        books = Book.objects.filter(category_id=selected_category)
    else:
        books = Book.objects.all()
    if search_query:

        books = books.filter(
            Q(title__icontains=search_query) |
            Q(book_description__icontains=search_query)|
            Q(author__icontains=search_query)
        )

    books_per_page = 8

    paginator = Paginator(books, books_per_page)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:

        books = paginator.page(1)
    except EmptyPage:

        books = paginator.page(paginator.num_pages)

    return render(request, 'layout/main.html', {'books': books, 'categories': categories})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'layout/book_detail.html', {'book': book})




'''
class SearchResultsView(ListView):
    model = Book
    context_object_name = 'books'
    ordering = ['title']
    #TODO paginate_by = 6

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
       
'''