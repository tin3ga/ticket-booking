from django.db import models
from django.conf import settings


# Create your models here.

class UserOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True)
    order_number = models.CharField(max_length=50, unique=True)
    payment_status = models.CharField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class Ticket(models.Model):
    customer = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50)
    event_name = models.CharField()
    tickets = models.IntegerField()
    ticket_type = models.CharField()

    def __str__(self):
        return f'{self.order_number} - {self.event_name}'
