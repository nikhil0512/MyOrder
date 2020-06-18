from django.conf.urls import url
from order.views import home


urlpattern = [
    url(r'^$', home),
]