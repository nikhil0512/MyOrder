from django.urls import path
from myorder.views import uploaddata, getItems, home, placeOrder

urlpatterns = [
    path('', home),
    path('getItems/', getItems),
    path('placeorder/', placeOrder),
    path('uploaddata/', uploaddata)
]