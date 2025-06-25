from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('inventory.urls')),  # or whatever app handles login
    path('home/', include('inventory.urls')),   # or whatever app handles home
    path('', lambda request: redirect('login')),  # 👈 Redirect root URL to /home/
    path('', include('inventory.urls')),
    

]
