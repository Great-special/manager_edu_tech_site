from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('courses/', views.course_list, name='courses'),
    path('categories/', views.get_categories, name='categories'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('category/<str:slug>/', views.category_detail, name='category_details'),
    
]