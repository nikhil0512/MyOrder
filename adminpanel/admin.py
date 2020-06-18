from django.contrib import admin
from django.contrib.admin import SimpleListFilter, ListFilter
from adminpanel.models import Items, Category, Store, StoreItem
from django.db.models import Q
from django.urls import path


admin.site.site_header = 'Admin Panel'

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(StoreItem)


class ItemFilter(SimpleListFilter):
    title = 'Category' # or use _('country') for translated title
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        items_obj = model_admin.model.objects.filter()
        #items = set([i.name for i in items_obj])
        return set([(c.category.id, c.category) for c in items_obj])

    def queryset(self, request, queryset):
        all_items = queryset.filter()
        category = request.GET.get('category', '')
        start_date = request.GET.get('created_on__gte', '')
        end_date = request.GET.get('created_on__lt', '')
        if category:
            all_items = all_items.filter(category=self.value())
        if start_date and end_date:
             all_items = all_items.filter(Q(created_on__gte=start_date), Q(created_on__lt=end_date))
        return all_items


# ModelAdmin Class # DataFlair
class ItemsA(admin.ModelAdmin):
    exclude = ('created_on', )
    list_display = ('name', 'unit', 'category')
    list_filter = (ItemFilter, 'created_on',)

    change_list_template = 'admin/change_list_items.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            #path('fontsize/<int:size>/', self.change_font_size)
        ]
        return custom_urls + urls

    def change_font_size(self):
        return 1


admin.site.register(Items, ItemsA)