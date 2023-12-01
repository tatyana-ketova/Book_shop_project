from django.shortcuts import render, redirect
from shop_app.form import CustomUserForm, Userprofile
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Book, Category, Cart, Favourite
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q
from django.http import JsonResponse
import json

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

            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user


            profile.save()
            registered = True
            messages.success(request,'Registeration Success you can Login Now!')
            return redirect('login')

        else:
            print(form.errors, profile_form.errors)
    else:
        form = CustomUserForm()
        profile_form = Userprofile()

    return render(request, 'layout/register.html',
                  {'form': form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            print("Username: {} and password: {}".format(username, password))

            if user:
                if user.is_active:
                    login(request, user)

                    print("Username: {} and password: {}".format(username, password))
                    messages.success(request,"You have logged in successfully")

                    return redirect('main')


                else:
                    return HttpResponse('Account not active')
            else:
                print("Someone try to login and failed")
                print("Username:{} and password{}".format(username, password))
                messages.error(request,"invalid login and password")
                return redirect('login')

        else:
            return render(request, 'layout/login.html', {})


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            book_qty = data['book_qty']
            book_id = data['pid']
            book_status = Book.objects.get(id=book_id)

            if book_status:
                if Cart.objects.filter(user=request.user.id,book_id = book_id):
                    return JsonResponse({'status':'Book Already added to Cart'}, status=200)
                else:
                    if book_status.quantity>=book_qty:
                        Cart.objects.create(user=request.user,book_id=book_id,book_qty=book_qty)
                        return JsonResponse({'status':'Book Added to Cart'}, status=200)
                    else:
                         return JsonResponse({'status':'Book Stock not avilable'}, status=200)
        else:
            return JsonResponse({'status':'Login To Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request,"layout/cart.html",{'cart':cart})
    else:
        return redirect('main')

def remove_cart(request,cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("cart")


def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            book_id = data['pid']
            book_status = Book.objects.get(id=book_id)
            if book_status:
                if Favourite.objects.filter(user=request.user.id,book_id = book_id):
                    return JsonResponse({'status':'Book Already added to Cart'}, status=200)
                else:
                    Favourite.objects.create(user=request.user,book_id=book_id)
                    return JsonResponse({'status':'Product Added to Favourite'}, status=200)
        else:
            return JsonResponse({'status':'Login To Add Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request,"layout/fav.html",{'fav':fav})
    else:
        return redirect('main')

def remove_fav(request,fid):
    item = Favourite.objects.get(id=fid)
    item.delete()
    return redirect("favpage")


def orderpage(request):
    return render(request,'layout/order.html')
