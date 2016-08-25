from django.conf.urls import url
from .views import register, user_login, user_logout, details


app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^(?P<account_id>[0-9]+)/$', details, name='details'),
]
