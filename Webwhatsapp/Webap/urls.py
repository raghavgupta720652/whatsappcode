from Webap import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse_lazy
from django.urls import path 

from .views import *

admin.autodiscover()

app_name = 'Webap'

urlpatterns = [
    
    url(r'^$', register, name='signup'),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add-phone/$', views.phone_add, name='add_phone'),
    url(r'^phone-data/$', PhoneListView.as_view(), name='phone_list'),
    url(r'^phone-delete/$', PhoneDelete.as_view(), name='phone_delete'),
    url(r'^send-message/$', PhoneSelectionSendView.as_view(), name='send_message'),
   
]
