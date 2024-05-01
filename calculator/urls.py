from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from calculator import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/create', views.ClientCreateView.as_view(), name='create_client'),
    path('clients/all', views.ClientListView.as_view(), name='clients'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('invoice/create', views.InvoiceCreateView.as_view(), name='create_invoice'),
    path('invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
]
