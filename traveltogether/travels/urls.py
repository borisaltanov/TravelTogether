from django.conf.urls import url
from .views import add_travel, detail, index, join_travel
urlpatterns = [
    url(r'^add_travel/$', add_travel, name='add_travel'),
    url(r'^(?P<travel_id>[0-9]+)/$', detail, name='detail'),
    url(r'^(?P<travel_id>[0-9]+)/join_success$', join_travel, name='join_travel'),
    url(r'^$', index, name='index')
]
