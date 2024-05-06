from django.urls import path, include
from users import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('me/', views.ProfileView.as_view(), name='me'),
    path('me/edit/', views.ProfileEditView.as_view(), name='edit'),

]
