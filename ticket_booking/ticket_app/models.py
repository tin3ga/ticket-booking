from django.db import models


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="event_images/")
    location = models.CharField(max_length=100)
    date = models.DateField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    vip_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/event/{self.slug}"
