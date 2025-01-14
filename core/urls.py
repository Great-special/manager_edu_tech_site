from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('', views.index_page, name='courses'),
    path('', views.index_page, name='course_detail'),
    path('<slug>/', views.index_page, name='category'),
]