from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from car_dealer_portal.models import CarDealer, Vehicles, Area
from customer_portal.models import Orders

# Inline admin for CarDealer
class CarDealerInline(admin.StackedInline):
    model = CarDealer
    can_delete = True
    verbose_name_plural = 'CarDealer'

# Extend the default User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CarDealerInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Area)
admin.site.register(Vehicles)
admin.site.register(Orders)
