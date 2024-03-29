from django import template

register = template.Library()


@register.filter
def placeholder(value, token):
    value.field.widget.attrs['placeholder'] = token
    return value


@register.filter
def rating_stars(rating):
    try:
        rating = int(rating)
    except ValueError:
        return ""

    full_stars = "★" * rating
    empty_stars = "☆" * (10 - rating)

    return full_stars + empty_stars
