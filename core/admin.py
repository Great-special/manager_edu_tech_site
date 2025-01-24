from django.contrib import admin
from .models import Category, Course, Testimonial, Payment, FeedBack
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'category', 'is_popular')
    list_filter = ('category', 'is_popular')
    search_fields = ('title',)
    ordering = ('title',)

class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title')
    search_fields = ('author_name',)
    ordering = ('author_name',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_customer', 'get_customer_email', 'get_customer_phone_number', 'amount', 'status')
    search_fields = ('get_customer', 'get_customer_email', 'get_customer_phone_number', 'amount',)
    ordering = ('-created_at',)
    
    def get_customer_email(self, obj):
        return obj.customer.email if obj.customer else 'N/A'
    
    def get_customer_phone_number(self, obj):
        return obj.customer.phone_number if obj.customer else 'N/A'

    def get_customer(self, obj):
        return obj.customer if obj.customer else 'N/A'



admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Testimonial, TestimonialsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(FeedBack)