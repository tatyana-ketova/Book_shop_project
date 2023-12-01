from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import SearchResultsView

urlpatterns = [

    path('', views.main, name="main"),
    path('layout/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', SearchResultsView.as_view(), name="search_results"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
