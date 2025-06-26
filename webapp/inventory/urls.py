from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('assets/', views.asset_list, name='asset_list'),
    path('book/', views.book_asset, name='book_asset'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('edit_booking/<str:pk>/', views.edit_booking, name='edit_booking'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.logout, name='logout'),
]


