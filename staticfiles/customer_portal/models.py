from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from car_dealer_portal.models import Area, CarDealer, Vehicles

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(
        validators=[MinLengthValidator(10), MaxLengthValidator(13)],
        max_length=13
    )
    # Jeśli chcesz, aby City/Pincode były opcjonalne, to dopuszczamy null/blank na area
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    # Dodane pola:
    age = models.PositiveIntegerField(null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(
        Vehicles,
        on_delete=models.SET_NULL,  # Zmiana z PROTECT na SET_NULL
        null=True,
        blank=True  # Opcjonalne, pozwala na pozostawienie pola pustego w formularzach
    )
    days = models.CharField(max_length=3)
    is_complete = models.BooleanField(default=False)