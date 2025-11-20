from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)  # store price as integer
    img = models.URLField(blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)  # new column

    #  Auto-calculate total price
    def save(self, *args, **kwargs):
        if self.price and self.guests:
            self.total_price = self.price * self.guests
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} - {self.date} {self.time}"
