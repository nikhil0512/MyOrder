from django.db import models
from adminpanel.models import Items
from customer.models import Customer


class Order(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)