from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100)
    hindiname = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        val = getattr(self, 'name', False)
        if val:
            setattr(self, 'name', val.capitalize())
        super(Category, self).save(*args, **kwargs)


class Items(models.Model):
    name = models.CharField(max_length=100)
    hindiname = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to='grokey_images', default='')
    sub_items = models.CharField(max_length=500, null=True, blank=True)
    tags = TaggableManager()
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = 'Item List'
        ordering = ['name']

    def __str__(self):
        return self.name

    def unit_as_list(self):
        return self.unit.split('/')

    def save(self, *args, **kwargs):
        val = getattr(self, 'name', False)
        if val:
            setattr(self, 'name', val.capitalize())
        super(Items, self).save(*args, **kwargs)


class Store(models.Model):
    storename = models.CharField(max_length=100)
    pin = models.IntegerField(default=000000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_created=True)

