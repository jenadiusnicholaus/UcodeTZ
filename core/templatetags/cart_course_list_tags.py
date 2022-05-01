from django import template
from core.models import CourseOrder

register = template.Library()


@register.inclusion_tag("base.html", takes_context=True)
def all_courses(context):
    course_list = CourseOrder.objects.all()[:3]

    return {'course_summary': context[course_list]}
