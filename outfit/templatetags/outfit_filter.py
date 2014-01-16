from django import template
from sell.models import condition_display

register = template.Library()

@register.filter
def primary_picture(value):
    """Given a set of pictures in value, return the picture that's marked as primary"""
    primary_picture = value.get(is_primary=True)
    return primary_picture.file.url

@register.filter
def primary_picture_thumbnail(value):
    """Given a set of pictures in value, return the picture that's marked as primary"""
    primary_picture = value.get(is_primary=True)
    return primary_picture.thumbnail_url

@register.filter
def picture_thumbnail_no_primary(value):
    pictures = value.filter(is_primary=False)
    return [pic.thumbnail_url for pic in pictures]

@register.filter
def get_condition_text(value):
    return condition_display[value]


