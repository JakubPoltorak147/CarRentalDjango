from car_dealer_portal.views import *
from django.urls import re_path as url

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^auth/$', auth_view, name='auth_view'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^add_vehicle/$', add_vehicle, name='add_vehicle'),
    url(r'^manage_vehicles/$', manage_vehicles, name='manage_vehicles'),
    url(r'^order_list/$', order_list, name='order_list'),
    url(r'^complete/$', complete, name='complete'),
    url(r'^history/$', history, name='history'),
    url(r'^delete/$', delete, name='delete'),
    url(r'^activate/(?P<token>[^/]+)/$', activate_account, name='activate_account'),
    url(r'^reset_password_request/$', reset_password_request, name='reset_password_request'),
    url(r'^reset_password_confirm/(?P<token>[^/]+)/$', reset_password_confirm, name='reset_password_confirm'),
    url(r'^update_profile/$', update_profile, name='update_profile'),
    url(r'^vehicle_detail/(?P<vehicle_id>\d+)/$', vehicle_detail, name='vehicle_detail'),
    url(r'^confirm_delete_vehicle/(?P<vehicle_id>\d+)/$', confirm_delete_vehicle, name='confirm_delete_vehicle'),
    url(r'^confirm_complete_order/(?P<order_id>\d+)/$', confirm_complete_order, name='confirm_complete_order'),
    url(r'^order_detail/(?P<order_id>\d+)/$', order_detail, name='order_detail'),
]
