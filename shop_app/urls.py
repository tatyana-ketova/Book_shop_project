from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.main,name="main"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
]
