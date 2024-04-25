from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from calculator import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/create', views.ClientCreateView.as_view(), name='create_client'),
    path('clients/all', views.ClientListView.as_view(), name='clients'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]
