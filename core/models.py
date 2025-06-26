from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, blank=True, null=True, unique=True)
    image = models.ImageField(_('image'), upload_to='category_images/', null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().title()
        # Automatically generate slug from name if not provided
        if self.name and not self.slug:
            self.slug = slugify(self.name.lower())
        super().save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    objectives = models.TextField(_('objectives'), blank=True, null=True, help_text="use comma separated items eg: Understand the fundamental concepts covered in this course, Develop skills relevant to the course subject matter")
    outlines = models.TextField(_('outlines'), blank=True, null=True, help_text="use column and comma separated items eg: Module 1:Introduction and Fundamentals, Module 2:Core Concepts and Principles")
    image = models.ImageField(_('image'), upload_to='course_images/', null=True, blank=True)
    goals = models.TextField(_('goals'), blank=True, null=True, help_text="use comma separated items eg: Provide comprehensive knowledge in the subject area, Prepare participants for industry challenges")
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    duration = models.CharField(_('duration'), max_length=50)
    category = models.ForeignKey(
        Category, 
        verbose_name=_('category'),
        on_delete=models.CASCADE, 
        related_name='courses'
    )
    mode = models.CharField(_('Course Mode'), max_length=150, blank=True, null=True)
    url = models.URLField(_('url'), null=True, blank=True)
    is_popular = models.BooleanField(_('is popular'), default=False)
    is_upcoming = models.BooleanField(_('is upcoming'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.title


class Testimonial(models.Model):  # Changed from plural to singular
    author_name = models.CharField(_('author name'), max_length=100)
    author_title = models.CharField(_('author title'), max_length=100, null=True, blank=True)
    author_image = models.ImageField(_('author image'), upload_to='testimonials/', null=True, blank=True)
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('testimonial')
        verbose_name_plural = _('testimonials')

    def __str__(self):
        return self.author_name


class EnrolledCustomer(models.Model):
    customer = models.CharField(max_length=255, verbose_name=_('customer'))
    email = models.EmailField(_('Email'))
    phone_number = models.CharField(_('Phone Number'), max_length=25, blank=True, null=True)
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    postcode = models.CharField(_('Postcode'), max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('Course'), related_name='courses')

    class Meta:
        verbose_name = _('enrolled_customer')
        verbose_name_plural = _('enrolled_customers')
    
    def __str__(self):
        return f"{self.customer} ({self.course.title})"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]
    
    customer = models.ForeignKey(EnrolledCustomer, on_delete=models.CASCADE, verbose_name=_('Customer'), related_name='customers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('amount'))
    currency = models.CharField(max_length=3, default='USD', verbose_name=_('currency'))
    quantity = models.IntegerField(_('Quantity'))
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name=_('status'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='', verbose_name=_('payment method'))
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, verbose_name=_('stripe payment intent id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at')) 
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
    
    def __str__(self):
        return f"{self.amount} {self.currency}"
    
class FeedBack(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('name'))
    email = models.EmailField(verbose_name=_('email'))
    message = models.TextField(verbose_name=_('message'))
    status = models.CharField(max_length=50, verbose_name=('status'), choices=(('Pending', 'Pending'), ('Attended', 'Attended')), default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.email})"
    
    
class CourseRegistration(models.Model):
    TITLE_CHOICES = [("Mr.", "Mr."), ("Mrs.", "Mrs."), ("Ms.", "Ms."), ("Dr.", "Dr.")]
    
    session = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations', verbose_name=_('course'))
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    designation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20)
    fax = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"