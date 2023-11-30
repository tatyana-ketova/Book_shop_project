from django.shortcuts import render, redirect
from shop_app.form import CustomUserForm, Userprofile
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q


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
            Q(book_description__icontains=search_query) |
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


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    registered = False

    if request.method == "POST":
        form = CustomUserForm(data=request.POST)
        profile_form = Userprofile(data=request.POST)

        if form.is_valid() and profile_form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            user = form.save(commit=False)

            if password == confirm_password:
                user.set_password(password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                registered = True
                messages.success(request, 'Registration successful. You can now login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')

        else:
            print(form.errors, profile_form.errors)
    else:
        form = CustomUserForm()
        profile_form = Userprofile()

    return render(request, 'layout/register.html',
                  {'form': form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        print("Username: {} and password: {}".format(username, password))

        if user:
            if user.is_active:
                login(request, user)

                messages.success(request, "You have logged in successfully")

                return HttpResponseRedirect(reverse('main'))

            else:
                return HttpResponse('Account not active')
        else:

            messages.success(request, "invalid login and password")
            return HttpResponseRedirect(reverse('login'))  # i need to add it to main

    else:
        return render(request, 'layout/login.html', {})
