from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<str:slug>', views.event, name='event'),
    path('tickets/', views.my_tickets, name='my_tickets'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

]
