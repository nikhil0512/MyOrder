from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.IntegerField()
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)