from django.http import HttpResponse
import stripe
from django.conf import settings
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Course, Category, Testimonial, Payment, FeedBack, EnrolledCustomer


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