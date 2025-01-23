from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    image = models.ImageField(_('image'), upload_to='course_images/', null=True, blank=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    duration = models.CharField(_('duration'), max_length=50)
    category = models.ForeignKey(
        Category, 
        verbose_name=_('category'),
        on_delete=models.CASCADE, 
        related_name='courses'
    )
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
    
    customer = models.CharField(max_length=255, verbose_name=_('customer'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('amount'))
    currency = models.CharField(max_length=3, default='USD', verbose_name=_('currency'))
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name=_('status'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name=_('payment method'))
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, verbose_name=_('stripe payment intent id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at')) 
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return f"{self.customer} - {self.amount} {self.currency}"
    
class FeedBack(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('name'))
    email = models.EmailField(verbose_name=_('email'))
    message = models.TextField(verbose_name=_('message'))
    status = models.CharField(max_length=50, verbose_name=('status'), choices=(('Pending', 'Pending'), ('Attended', 'Attended')), default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.email})"    