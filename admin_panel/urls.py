from django.urls import path, include

from admin_panel import views

urlpatterns = [
    path('', views.SuperuserView.as_view(), name='superuser_view'),
    path('manage_users', views.SuperuserUsersView.as_view(), name='manage_users'),
    path('manage-users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('manage-users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('manage-users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('manage_clients', views.SuperuserClientsView.as_view(), name='manage_clients'),
    path('manage_invoices', views.SuperuserInvoicesView.as_view(), name='manage_invoices'),
]
