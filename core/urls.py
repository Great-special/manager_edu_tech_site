from django.urls import path
from . import views



urlpatterns = [
    path('', views.index_page, name='home'),
    path('search/', views.search_courses, name='search'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('courses/', views.course_list, name='courses'),
    path('services/', views.services_page, name='services'),
    path('categories/', views.get_categories, name='categories'),
    path('professional-skills/', views.professional_skills, name='professional_skills'),
    path('technical-training/', views.technical_training, name='technical_training'),
    path('leadership-development/', views.leadership_development, name='leadership_development'),
    path('digital-marketing/', views.digital_marketing, name='digital_marketing'),
    path('project-management/', views.project_management, name='project_management'),
    path('upskilling-reskilling/', views.upskilling_reskilling, name='upskilling_reskilling'),
    path('certification/', views.certification, name='certification'),
    path('consultancy/', views.consultancy, name='consultancy'),
    path('online-courses/', views.get_online_courses, name='online_courses'),
    path('classroom-courses/', views.get_classroom_courses, name='classroom_courses'),
    path('executive-courses/', views.get_executive_courses, name='executive_courses'),
    path('bespoke-courses/', views.get_bespoke_courses, name='bespoke_courses'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('category/<str:slug>/', views.category_detail, name='category_details'),
    path('register-course/', views.register_course, name='register_course'),
    path('payment-checkout/<int:id>/', views.payment_page, name='payment_page'),
    path("create-checkout-session/<int:id>/", views.createstripe_checkout_session, name="create_checkout_session"),
    
    path('upload-csv/', views.upload_csv_courses, name='upload_csv_courses'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
    
]