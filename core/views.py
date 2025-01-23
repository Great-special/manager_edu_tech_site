import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Category, Testimonial, Payment, FeedBack


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def index_page(request):
    try:
        categories = Category.objects.all()
        popular_courses = Course.objects.filter(is_popular=True)
    except Exception as e:
        print(e)
        categories = None
        popular_courses = None
    
    try:
        testimonials = Testimonial.objects.all()
    except:
        testimonials = []
    
    context = {
        'categories': categories, 
        'popular_courses': popular_courses,
        'testimonials':testimonials
    }
    return render(request, 'ihrdc_layout/index.html', context)

def course_list(request):
    try:
        categories = Category.objects.all()
        courses = Course.objects.all()
    except Exception as e:
        print(e)
        categories = None
        courses = None
    return render(request, 'ihrdc_layout/courses.html', {'courses': courses, 'categories': categories})

def course_detail(request, id):
    course = Course.objects.get(id=id)
    return render(request, 'ihrdc_layout/course_detail.html', {'course': course})

def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    courses = Course.objects.filter(category=category)
    return render(request, 'ihrdc_layout/category.html', {'courses':courses, 'category':category})

def get_categories(request):
    categories = Category.objects.all()
    return render(request, 'ihrdc_layout/categories.html', {'categories':categories})

def about_page(request):
    return render(request, 'ihrdc_layout/about.html')

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        FeedBack.objects.create(
            name=name,
            email=email,
            message=message
        )
        return render(request, 'ihrdc_layout/thank_you.html')
    return render(request, 'ihrdc_layout/contact.html')


def payment_page(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'ihrdc_layout/course_payment.html', {'stripe_key': settings.STRIPE_PUBLIC_KEY, 'course':course})

