from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
#from .views import SearchResultsView

urlpatterns = [

    path('', views.main, name="main"),
    path('layout/<int:book_id>/', views.book_detail, name='book_detail'),
    path('register',views.register,name="register"),
    path('login',views.user_login,name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart/',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('fav',views.fav_page,name="fav"),
    path('favpage',views.favviewpage,name="favpage"),
    path('order',views.orderpage,name="order"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
