from django.urls import path
from django.conf.urls import url
from adminpanel.views import uploaddata, getItems, home, placeOrder, uploaddatatemp, items_snippet

urlpatterns = [
    url(r'^$', home),
    url(r'^getItems/', getItems),
    url(r'^placeorder/', placeOrder),
    url(r'^upload_data/', uploaddata),
    url(r'^uploaddatatemp/', uploaddatatemp),
    url(r'^items_snippet/(?P<category_id>[- \d]+)/(?P<item_name>[- \d\w]+)/$', items_snippet)
]