import csv
from typing import Type
from django.db import transaction
from django.db.models import Model
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import stripe
from django.conf import settings
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Course, Category, Testimonial, Payment, FeedBack, EnrolledCustomer
from .forms import CSVFileUploadForm, FieldMappingFormset


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

def professional_training(request):
    context = {
        'page_title': 'Professional Training',
        'description': 'Our industry-specific courses are meticulously designed by experts to provide cutting-edge knowledge and skills.',
        'lists': [
            'Tailored Learning Paths',
            'Expert-Led Courses',
            'Industry-Current Curriculum',
            'Flexible Learning Options'
        ]
    }
    return render(request, 'ihrdc_layout/what_we_do_details.html', context)

def upskilling_reskilling(request):
    context = {
        'page_title': 'Upskilling & Reskilling',
        'description': 'Adapt to the changing business landscape by re-tooling your skillsets and expanding your professional capabilities.',
        'lists': [
            'Adaptive Learning Strategies',
            'Career Transformation Support',
            'Emerging Technology Focus',
            'Personalized Skill Development'
        ]
    }
    return render(request, 'ihrdc_layout/what_we_do_details.html', context)

def certification(request):
    context = {
        'page_title': 'Professional Certification',
        'description': 'Earn internationally recognized certifications that validate your expertise and enhance your professional credibility.',
        'lists': [
            'Technical Certifications',
            'Professional Development Credentials',
            'Industry-Specific Qualifications',
            'Global Recognition Programs'
        ]
    }
    return render(request, 'ihrdc_layout/what_we_do_details.html', context)

def consultancy(request):
    context = {
        'page_title': 'Expert Consultancy',
        'description': 'Rapid, targeted consulting to resolve organizational bottlenecks and drive strategic improvements.',
        'lists': [
            'Strategic Planning',
            'Process Optimization',
            'Technology Integration',
            'Performance Enhancement'
        ]
    }
    return render(request, 'ihrdc_layout/what_we_do_details.html', context)

def import_csv_to_model(csv_file_path: str, model_class: Type[Model], field_mapping: dict = {}, skip_header: bool = True) -> tuple[int, list]:
    """
    Import data from a CSV file into a Django model, saving records one by one.
    
    Args:
        csv_file_path (str): Path to the CSV file
        model_class (Type[Model]): Django model class to create instances of
        field_mapping (dict, optional): Dictionary mapping CSV headers to model fields.
            If empty, assumes CSV headers match model field names.
        skip_header (bool, optional): Whether to skip the first row. Defaults to True.
    
    Returns:
        tuple[int, list]: Number of records created and list of errors encountered.
    
    Example:
        field_mapping = {
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Email Address': 'email'
        }
        created, errors = import_csv_to_model(
            'users.csv', 
            UserModel, 
            field_mapping
        )
    """
    records_created = 0
    errors = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            # Skip header if required
            if skip_header:
                next(csv_reader, None)

            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    # Transform data according to field mapping
                    if field_mapping:
                        transformed_data = {
                            model_field: row[csv_field]
                            for csv_field, model_field in field_mapping.items()
                            if csv_field in row
                        }
                    else:
                        transformed_data = row
                    
                    # Create and validate model instance
                    instance = model_class(**transformed_data)
                    instance.full_clean()  # Validate data
                    with transaction.atomic():  # Ensure transaction safety
                        instance.save()
                    
                    records_created += 1
                
                except (ValidationError, KeyError) as e:
                    errors.append(f"Error in row {row_number}: {str(e)}")
                except Exception as e:
                    errors.append(f"Unexpected error in row {row_number}: {str(e)}")
    
    except FileNotFoundError:
        errors.append(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        errors.append(f"Error processing CSV file: {str(e)}")
        
    return records_created, errors

def upload_csv_courses(request):
    if request.method == "POST" and request.FILES:
        file_form = CSVFileUploadForm(request.POST, request.FILES)
        mapping_formset = FieldMappingFormset(request.POST, prefix='mappings')

        if file_form.is_valid() and mapping_formset.is_valid():
            try:
                # Get the uploaded file
                csv_file = request.FILES['csv_file']

                # Save file temporarily
                temp_path = default_storage.save(
                    f'temp/{csv_file.name}',
                    ContentFile(csv_file.read())
                )
                file_path = default_storage.path(temp_path)

                # Create field mapping dictionary from formset
                field_mapping = {
                    form.cleaned_data['csv_column']: form.cleaned_data['model_field']
                    for form in mapping_formset
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                }

                try:
                    # Import CSV data using the previous import_csv_to_model function
                    records_created, errors = import_csv_to_model(
                        csv_file_path=file_path,
                        model_class=Category,  # Replace with your model
                        field_mapping=field_mapping
                    )

                    # Handle results
                    if errors:
                        for error in errors:
                            messages.warning(request, error)
                    
                    messages.success(
                        request,
                        f'Successfully created {records_created} records'
                    )

                except Exception as e:
                    messages.error(request, f'Error processing file: {str(e)}')

                finally:
                    # Clean up - delete temporary file
                    default_storage.delete(temp_path)

                return redirect('success_url')  # Replace with your success URL

            except Exception as e:
                messages.error(request, f'Error handling file: {str(e)}')
                return redirect('upload_csv_courses')
    else:
        file_form = CSVFileUploadForm()
        mapping_formset = FieldMappingFormset(prefix='mappings')

    context = {
        'file_form': file_form,
        'mapping_formset': mapping_formset
    }
    return render(request, 'ihrdc_layout/upload_csv.html', context)
            
        



def payment_page(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'ihrdc_layout/course_payment.html', {'stripe_key': settings.STRIPE_PUBLIC_KEY, 'course':course})


def createstripe_checkout_session(request, id):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """
 
    current_domain = request.build_absolute_uri('/')
    print(current_domain)
    course = Course.objects.get(id=id)

    if request.method == 'POST':
        customer = request.POST.get('customer', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        country = request.POST.get('country', '')
        postcode = request.POST.get('postcode', '')     
        quantity = request.POST.get('quantity', 1)
        currency = request.POST.get('currency', 'USD')
    
    try:
        image_url = course.image.url
    except:
        image_url = ''
    
    # creating enrolled customer
    enrolled = EnrolledCustomer.objects.create(
        customer=customer,
        email=email,
        phone_number=phone,
        city=city,
        country=country,
        postcode=postcode,
        course=course
    )
    enrolled.save()
    
    # creating payment history
    transaction = Payment.objects.create(
        customer=enrolled,
        currency = currency,
        amount = int(course.price) * int(quantity),
        quantity = quantity,      
    )
    transaction.save()
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card", "us_bank_account"],
        line_items=[
            {
                "price_data": {
                    "currency": str(currency).lower(),
                    "unit_amount": int(course.price) * 100,
                    "product_data": {
                        "name": course.title,
                        "description": course.description,
                        "images": [
                            f"{current_domain}/{image_url}"
                        ],
                    },
                },
                "quantity": int(quantity),
            }
        ],
        metadata={"product_id": course.id, 'payment_id': transaction.id},
        mode="payment",
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return redirect(checkout_session.url)


def success(request):
    return render(request, "ihrdc_layout/success.html")


def cancel(request):
    return render(request, "ihrdc_layout/cancel.html")

@method_decorator(csrf_exempt, name="dispatch")
def stripe_webhook(request, format=None):
    """
    Stripe webhook view to handle checkout session completed event.
    """
    payload = request.body
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        print("Payment successful")

        # Add this
        session = event["data"]["object"]
        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        product = get_object_or_404(Course, id=product_id)
        payment_id = session["metadata"]["payment_id"]
        payment = get_object_or_404(Payment, id=payment_id)
        payment.payment_status = "completed"
        payment.save()
        
        # send_mail(
        #     subject="Here is your product",
        #     message=f"Thanks for your purchase. The URL is: {product.url}",
        #     recipient_list=[customer_email],
        #     from_email="your@email.com",
        # )

    return HttpResponse(status=200)