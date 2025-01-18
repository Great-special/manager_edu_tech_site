from django.shortcuts import render
from .models import Course, Category

# Create your views here.


def index_page(request):
    try:
        categories = Category.objects.all()
        popular_courses = Course.objects.filter(is_popular=True)
    except Exception as e:
        print(e)
        categories = None
        popular_courses = None
    return render(request, 'ihrdc_layout/index.html', {'categories': categories, 'popular_courses': popular_courses})

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
    return render(request, 'ihrdc_layout/contact.html')