from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('search/', views.search_courses, name='search'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('courses/', views.course_list, name='courses'),
    path('categories/', views.get_categories, name='categories'),
    path('professional-training/', views.professional_training, name='professional_training'),
    path('upskilling-reskilling/', views.upskilling_reskilling, name='upskilling_reskilling'),
    path('certification/', views.certification, name='certification'),
    path('consultancy/', views.consultancy, name='consultancy'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('category/<str:slug>/', views.category_detail, name='category_details'),
    path('payment-checkout/<int:id>/', views.payment_page, name='payment_page'),
    path("create-checkout-session/<int:id>/", views.createstripe_checkout_session, name="create_checkout_session"),
    
    path('upload-csv/', views.upload_csv_courses, name='upload_csv_courses'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
    
]