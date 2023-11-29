from django.shortcuts import render, redirect
from shop_app.form import CustomUserForm, Userprofile
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def main(request):
    return render(request, 'layout/main.html')


#def login(request):
    #return render(request, 'layout/Login.html')
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

            if 'image' in request.FILES:
                profile.image = request.FILES["image"]

            profile.save()
            registered = True
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

                print("Username: {} and password: {}".format(username, password))
                return HttpResponseRedirect(reverse('main'))


            else:
                return HttpResponse('Account not active')
        else:
            print("Someone try to login and failed")
            print("Username:{} and password{}".format(username, password))
            return HttpResponse("invalid login and password")

    else:
        return render(request, 'layout/login.html', {})
