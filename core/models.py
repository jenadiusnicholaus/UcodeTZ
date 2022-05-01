from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from authentication.models import User
from ucodetz import settings
from django_countries.fields import CountryField

COURSE_LEVEL_CHOICE = (
    ('F', 'Free'),
    ('P', 'pro'),
)
COURSE_STATUS = (
    ('0', 'save to Draft'),
    ('1', 'Publish'),
)
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

region = {

    ('Ar', 'Arusha'),
    ('Dar', 'Dar es salaam'),
    ('Mw', 'Mwanza'),
    ('Mb', 'Mbeya'),
}


class Topics(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=100, null=True)
    content = models.TextField(null=True)
    create = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.title


# Categories
class Category(models.Model):
    name = models.CharField(max_length=30, null=True)
    icon_label = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Courses(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='course-image', null=True)
    title = models.CharField(max_length=200, null=True)
    content = RichTextField(verbose_name='course desc', null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    discount_price = models.FloatField(blank=True, null=True)
    short_desc = models.TextField(null=True)
    slug = models.SlugField(max_length=200, null=True)
    # student = models.ManyToManyField(User, related_name='Enrolled')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL, null=True)
    course_level = models.CharField(max_length=200, null=True, choices=COURSE_LEVEL_CHOICE)
    status = models.CharField(max_length=200, null=True, choices=COURSE_STATUS)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:course-details", kwargs={'slug': self.slug})

    def get_add_to_cart(self):
        return reverse('add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def enrolled(self):
        total: int = 0
        try:
            for enl in self.student.all():
                total = enl
        except:
            return None
        return total


class Enrollment(models.Model):
    student = models.ManyToManyField(User, related_name='Enrolled')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Enrollment'

    def __str__(self):
        return str(self.course.title)

    def get_course_image(self):
        try:
            return self.course.image.url
        except:
            return None

    def get_course_description(self):
        try:
            return self.course.short_desc
        except:
            return None

    def get_course_category(self):
        try:
            return self.course.category.name
        except:
            return None

    def enrolled_student(self):
        enrolled_total = 0
        try:
            for enrolled_std in self.student.all():
                enrolled_total = enrolled_std.student.count()
        except:
            return 0
        return enrolled_total


class EnrolledCourse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, )
    paid = models.BooleanField(default=False)
    updated_on = models.DateTimeField(default=timezone.now, null=True, )

    class Meta:
        verbose_name_plural = 'Enrolled Course'

    def __abs__(self):
        return self.course.course_title

    def get_total_course_price(self):
        return self.course.price

    def get_total_discount_course_price(self):
        return self.course.discount_price

    def get_final_price(self):
        if self.course.discount_price:
            return self.get_total_discount_course_price()
        return self.get_total_course_price()


class CourseOrder(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(EnrolledCourse)
    created_on = models.DateTimeField(default=timezone.now, null=True, )
    updated_on = models.DateTimeField(default=timezone.now, null=True, )
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'My Course list'

    def __abs__(self):
        return self.student

    def __str__(self):
        return str(self.student)

    def get_total(self):
        try:
            total = 0
            for order_course in self.courses.all():
                total += order_course.get_final_price()
            # if self.coupon:
            #     total -= self.coupon.amount
            return total
        except:
            return None


class BillingAddress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    country = CountryField()
    region = models.CharField(max_length=10, choices=region, null=True)
    payment_method = models.CharField(max_length=20, null=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Billing address'


class Payments(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Payments'
