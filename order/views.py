from adminpanel.models import Items, Category
from django.shortcuts import render
from Nikhil.settings import BASE_DIR


def home(request):
    items = Items.objects.all()
    categories = Category.objects.all()
    return render(request, 'myorder.html',
                  context={'items': items, 'categories': categories, 'base': BASE_DIR})