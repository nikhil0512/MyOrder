from django.urls import path
from django.conf.urls import url
from adminpanel.views import uploaddata, getItems, home, home1, placeOrder, uploaddatatemp, items_snippet

urlpatterns = [
    url(r'^$', home1),
    url(r'^home/(?P<slug>[- \d\w]+)/$', home),
    url(r'^getItems/', getItems),
    url(r'^placeorder/', placeOrder),
    url(r'^uploaddata/', uploaddata),
    url(r'^uploaddatatemp/', uploaddatatemp),
    url(r'^items_snippet/(?P<slug>[- \d\w]+)/(?P<category_id>[- \d]+)/(?P<item_name>[- \d\w]+)/$', items_snippet)
]