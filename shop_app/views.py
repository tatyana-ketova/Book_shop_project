from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, CustomerRegisterForm

def home(request):
    return render(request, 'layout/index.html')

def register(request):
    if request.method == 'POST':
        form_user = UserRegisterForm(request.POST)
        form_customer = CustomerRegisterForm(request.POST)
        if form_user.is_valid() and form_customer.is_valid():
            user = form_user.save()
            user.refresh_from_db()
            form_customer = CustomerRegisterForm(request.POST, instance=user.customer)
            form_customer.full_clean()

            customer = form_customer.save(commit=False)
            customer.user = user
            customer.save()

            username = form_user.cleaned_data.get('username')
            phone = form_customer.cleaned_data.get('phone')
            messages.success(request, f'Account created for {username}(#{phone}) so you can log in!')
            return redirect('login')
    else:
        form_user = UserRegisterForm()
        form_customer = CustomerRegisterForm()
    return render(request, 'layout/register.html', {'form_user':form_user, 'form_customer': form_customer})


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

class SearchResultsView(ListView):
    model = Book
    template_name = 'layout/search_results.html'
    context_object_name = 'books'
    ordering = ['title']
    paginate_by = 8

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




