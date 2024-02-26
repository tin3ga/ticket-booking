from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:event_id>', views.add_to_cart, name='add_to_cart'),

]
