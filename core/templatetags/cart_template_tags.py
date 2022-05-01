from django import template
from core.models import CourseOrder

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = CourseOrder.objects.filter(student=user, paid=False)
        if qs.exists():
            return qs[0].courses.count()
    return 0
