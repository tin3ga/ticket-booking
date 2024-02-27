from django.contrib import admin

from .models import UserOrder, Ticket

# Register your models here.

admin.site.register(UserOrder)
admin.site.register(Ticket)
