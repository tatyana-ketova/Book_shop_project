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

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
