from django.shortcuts import render, redirect
from shop_app.form import customUserForm,userprofile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def main(request):
    return render(request,'layout/main.html')
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect('/')    


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
 
        user = authenticate(request, username=username, password=password)
 
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main'))
            else:
                return HttpResponse('Account not active')
        else:
            # Log the failed login attempt
            print("Someone tried to login and failed")
            print("Username: {} and password: {}".format(username, password))
 
            return HttpResponse("Invalid login credentials")
    else:
        # This is a GET request, render the login form
        return render(request, 'layout/login.html', {})


def register(request):
    registered = False
    form = customUserForm()

    if request.method == "POST":
        form = customUserForm(data=request.POST)
        profile_form = userprofile(data=request.POST)
        
        if form.is_valid() and profile_form.is_valid():

            user=form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered  = True
            messages.success(request,'Your registration is success....')
            return redirect('login')
        else :
            print(form.errors,profile_form.errors)
            
    else:
        form = customUserForm()
        profile_form = userprofile()
     
    return render(request, 'layout/register.html',{'form':form,'profile_form':profile_form,'registered':registered})





           
    
