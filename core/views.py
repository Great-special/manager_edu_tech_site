from django.shortcuts import render
from .models import Course, Category

# Create your views here.


def index_page(request):
    return render(request, 'ihrdc_layout/index.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'ihrdc_layout/course_list.html', {'courses': courses})

def course_detail(request, id):
    course = Course.objects.get(id=id)
    return render(request, 'ihrdc_layout/course_detail.html', {'course': course})

def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    courses = Course.objects.get(category=category)
    return render(request, 'ihrdc_layout/category_detail.html', {'courses':courses, 'category':category})


def about_page(request):
    return render(request, 'ihrdc_layout/about.html')

def contact_page(request):
    return render(request, 'ihrdc_layout/contact.html')