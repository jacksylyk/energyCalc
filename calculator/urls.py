from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from calculator import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/create', views.ClientCreateView.as_view(), name='create_client'),
    path('clients/all', views.ClientListView.as_view(), name='clients'),
]
