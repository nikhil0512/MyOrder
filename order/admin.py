import site

from django.contrib import admin
from order.models import Order
from customer.models import Customer


@admin.register(Order, site='')
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'admin/snippets/snippets_change_list.html'
    pass