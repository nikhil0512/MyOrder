from django import template

register = template.Library()


@register.simple_tag
def get_item_image(item_obj):
    try:
        return item_obj.image_url.url
    except:
        return ''