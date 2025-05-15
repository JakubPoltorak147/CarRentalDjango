from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer_portal/',include('customer_portal.urls')),
    path('car_dealer_portal/',include('car_dealer_portal.urls')),
    path('',include('home.urls')),
]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
