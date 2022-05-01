from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.base import View

from core.forms import CheckoutForm
from core.models import *


class CourseView(View):
    def get(self, *args, **kwargs):
        course_qs = Courses.objects.all()
        popular_course = Enrollment.objects.filter()
        context = {
            'course_list': course_qs,
            'popular_course': popular_course,
        }
        return render(self.request, template_name='course.html', context=context)


class CourseIntroduction(View):

    def get_enrolled_student(self, slug):
        course = get_object_or_404(Courses, slug=slug)
        total = 0
        for enrolled in course.enrollment_set.all():
            total = enrolled.student.count()
        return total

    def get(self, request, slug, *args, **kwargs):
        course_order = CourseOrder.objects.filter(student=request.user, paid=False)
        course = get_object_or_404(Courses, slug=slug)

        context = {
            "course_list": course,
            'enllored': self.get_enrolled_student(slug=course.slug)
        }
        if course_order.exists():
            order = course_order[0]
            if order.courses.filter(course__slug=course.slug).exists():
                messages.info(request, " continue to checkout")
                # return render(request, template_name='pricing.html', context=context)
                return render(request, template_name='course_intro.html', context=context)
            else:
                return render(request, template_name='course_intro.html', context=context)

        else:
            return render(request, template_name='course_intro.html', context=context)


def chech_enrolled_student(course, user):
    enrollment_qs = Enrollment.objects.filter(course__slug=course.slug)
    if enrollment_qs.exists():
        enrolled = enrollment_qs[0]
        if enrolled.student.filter(Enrolled=user).exists():
            return redirect('checkout')
        else:
            enrolled.student.add(user)

            return redirect('course')
    else:
        enrollment, create = Enrollment.objects.get_or_create(
            course=course,
        )
        enrollment.student.add(user)
        return redirect('caourse')


@login_required()
def add_to_cart(request, slug):
    if request.user.is_authenticated:
        course = get_object_or_404(Courses, slug=slug)

        enrolled_course, created = EnrolledCourse.objects.get_or_create(
            student=request.user,
            course=course,

        )

        enrollment, create = Enrollment.objects.get_or_create(
            course=course,

        )
        enrollment.student.add(request.user)

        # Todo  check  a user is already enrollments

        order_qs = CourseOrder.objects.filter(student=request.user, paid=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.courses.filter(course__slug=course.slug).exists():
                enrolled_course.save()
                messages.success(request, 'This item quantity was updated ')
                return redirect('cart', )
            else:

                order.courses.add(enrolled_course)
                messages.success(request, 'This item was added to your cart ')
                return redirect('cart', )

        else:

            order = CourseOrder.objects.create(
                student=request.user
            )
            order.courses.add(enrolled_course)

            messages.success(request, 'this item was added to your cart ')
            return redirect('cart')

    else:
        item = get_object_or_404(Courses, slug=slug)
        order_item, created = EnrolledCourse.objects.get_or_create(
            user=None,
            item=item,
        )
        print(order_item)

        order_qs = Cart.objects.filter(user=None, ordered=False, session_key=request.session.session_key)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.products.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                print("1")
            else:
                order.products.add(order_item)
        else:
            order = Cart.objects.create(
                user=None, session_key=request.session.session_key
            )
            order.products.add(order_item)
            print("done")
        return redirect("cart:home")


class Cart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = CourseOrder.objects.get(student=self.request.user, paid=False)
            context = {
                'cart_object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


#
class Checkout(View):
    def get(self, request, *args, **kwargs):
        course_ordsed = CourseOrder.objects.get(student=request.user, paid=False)
        form = CheckoutForm()
        context = {
            'course_order': course_ordsed,
            'form': form
        }
        return render(request, template_name='checkout.html', context=context)

    def post(self, request, *args, **kwargs):
        course_ordsed = CourseOrder.objects.get(student=request.user, paid=False)
        context = {
            'course_order': course_ordsed
        }
        messages.info(request, 'ready to go')
        return render(request, template_name='checkout.html', context=context)


def course_progress(request):
    return render(request, template_name='course_progress.html')


def course_lesson(request):
    return render(request, template_name='course_lesson.html')


def course_path(request):
    return render(request, template_name='course_path.html')


def course_path_level(request):
    return render(request, template_name='course_path_level.html')


def profile(request):
    return render(request, template_name='profile.html')


def profile_edit(request):
    return render(request, template_name='profile_edit.html')


def blog(request):
    return render(request, template_name='blog.html')


def pricing(request):
    return render(request, template_name='pricing.html')


def terms(request):
    return render(request, template_name='terms.html')


def coming_soon(request):
    return render(request, template_name='coming_soon.html')


def books(request):
    return render(request, template_name='books.html')


def book_description(request):
    return render(request, template_name='book_descriptions.html')


def episodes(request):
    return render(request, template_name='episodes.html')


def episodes_details(request):
    return render(request, template_name='episode_details.html')


def faq(request):
    return render(request, template_name='faq.html')

