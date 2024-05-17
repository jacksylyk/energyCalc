from django.urls import path, include

from admin_panel import views

urlpatterns = [
    path('', views.SuperuserView.as_view(), name='superuser_view'),
    path('manage_users', views.SuperuserUsersView.as_view(), name='manage_users'),
    path('manage_users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('manage_users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('manage_users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('manage_users/reset-password/<int:pk>/', views.UserResetPasswordView.as_view(), name='reset_password'),
    path('manage_clients', views.SuperuserClientsView.as_view(), name='manage_clients'),
    path('manage_clients/update/<int:pk>/', views.ClientUpdateView.as_view(), name='client_update'),
    path('manage_clients/delete/<int:pk>/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('manage_invoices', views.SuperuserInvoicesView.as_view(), name='manage_invoices'),
    path('manage_invoices/delete/<int:pk>/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
]
