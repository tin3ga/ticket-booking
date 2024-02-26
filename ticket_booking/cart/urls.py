from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:event_id>', views.add_to_cart, name='add_to_cart'),
    path('delete/<int:event_id>', views.delete_from_cart, name="delete_from_cart"),

]
