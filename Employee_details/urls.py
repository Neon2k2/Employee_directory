from django.contrib import admin
from django.urls import path, include
from firstapp.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstapp.urls')),
]
