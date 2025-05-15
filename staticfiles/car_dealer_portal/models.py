from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User

class Area(models.Model):
    pincode = models.CharField(
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
        max_length=6
    )
    city = models.CharField(max_length=20)

    class Meta:
        unique_together = ('city', 'pincode')

    def __str__(self):
        return f"{self.city} ({self.pincode})"

class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(
        validators=[MinLengthValidator(10), MaxLengthValidator(13)],
        max_length=13
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.car_dealer.username

class Vehicles(models.Model):
    car_name = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    capacity = models.CharField(max_length=2)
    is_available = models.BooleanField(default=True)
    description = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    # Zamiast URLField użyjemy ImageField:
    photo = models.ImageField(upload_to='vehicles/', null=True, blank=True)

    def __str__(self):
        return f"{self.car_name} - {self.color}"
