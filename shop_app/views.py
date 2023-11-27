from django.shortcuts import render, redirect
from shop_app.form import customUserForm,userprofile

from django.contrib import messages


def main(request):
    return render(request,'layout/main.html')
def login(request):
    return render(request,'layout/Login.html')
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

            if 'image' in request.FILES:
                profile.image = request.FILES["image"]

            profile.save()
            registered  = True
        else :
            print(form.errors,profile_form.errors)
    else:
        form = customUserForm()
        profile_form = userprofile()
     
    return render(request, 'layout/register.html',{'form':form,'profile_form':profile_form,'registered':registered})




           
    
