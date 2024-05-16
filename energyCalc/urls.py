from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculator.urls')),
    path('users/', include('users.urls')),
    path('superuser/', include('admin_panel.urls')),
]
