from django.urls import path
from . import views
app_name = 'customer_portal'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('auth/', views.auth_view, name='auth_view'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('registration/', views.registration, name='registration'),
    path('activate/<str:token>/', views.activate_account, name='activate_account'),

    path('reset_password_request/', views.reset_password_request, name='reset_password_request'),
    path('reset_password_confirm/<str:token>/', views.reset_password_confirm, name='reset_password_confirm'),

    path('update_profile/', views.update_profile, name='update_profile'),

    # Twoje istniejące widoki:
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('rent_vehicle/', views.rent_vehicle, name='rent_vehicle'),
    path('confirm/', views.confirm, name='confirm'),
    path('manage/', views.manage, name='manage'),
    path('update_order/', views.update_order, name='update_order'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('all_cars/', views.all_cars, name='all_cars'),
    # Strona szczegółów o danym samochodzie
    path('vehicle_details/<int:vehicle_id>/', views.vehicle_details, name='vehicle_details'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]


