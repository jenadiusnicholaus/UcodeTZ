from django.urls import path
from . import views

urlpatterns = [
    # path('dasgboard/', views.home, name='dashboard'),
    path('course/', views.CourseView.as_view(), name='course'),
    path('course_path/', views.course_path, name='course-path'),
    path('course_level/', views.course_path_level, name='course_path_level'),
    path('course_intro/<slug>', views.CourseIntroduction.as_view(), name='course_intro'),
    path('course_progress/', views.course_progress, name='course_progress'),
    path('course_lesson/', views.course_lesson, name='course_lesson'),
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    # path('login/', views.login, name='login'),
    # path('', views.register, name='register'),
    # path('blog/', views.blog, name='blog'),
    path('pricing/', views.pricing, name='pricing'),
    path('terms/', views.terms, name='terms'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('books/', views.books, name='books'),
    path('book_description/', views.book_description, name='book_description'),
    path('episodes/', views.episodes, name='episodes'),
    path('episodes_details/', views.episodes_details, name='episodes_details'),
    path('faq/', views.faq, name='faq'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    # process order
    path('add_to_cart/<slug:slug>', views.add_to_cart, name='add_to_cart'),

]
