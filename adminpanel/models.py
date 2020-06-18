from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify


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


def get_grocery_images(instance, filename):
    return 'images/%d/%s' % (instance.name, filename)


class Items(models.Model):
    name = models.CharField(max_length=100)
    hindiname = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to=get_grocery_images, default='')
    sub_items = models.CharField(max_length=500, null=True, blank=True)
    tags = TaggableManager()
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True, auto_created=True)

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
    pin = models.IntegerField(default=000000, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_created=True, blank=True, null=True)
    slug = models.SlugField(max_length=140, unique=True)

    def _get_unique_slug(self):
        slug = slugify(self.storename)
        unique_slug = slug
        num = 1
        while Items.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.storename


class StoreItem(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,blank=True, null=True)

