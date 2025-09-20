from django.contrib import admin
from .models import Category, Course, Testimonial, Payment, FeedBack, CourseRegistration, AccessModel
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



class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)



class AccessModelAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Testimonial, TestimonialsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(FeedBack)
admin.site.register(CourseRegistration)



admin.site.site_header = 'i-Citadel Admin'
admin.site.site_title = 'i-Citadel Admin Portal'
admin.site.index_title = 'Welcome to i-Citadel Admin Portal'




class AdminSetUp(admin.AdminSite):
    site_header = 'i-Citadel Admin'
    site_title = 'i-Citadel Admin Portal'
    index_title = 'Welcome to i-Citadel Admin Portal'
    

admin_set_up = AdminSetUp(name='dev-admin')
admin_set_up.register(Category, CategoryAdmin)
admin_set_up.register(Course, CourseAdmin)  
admin_set_up.register(Testimonial, TestimonialsAdmin)
admin_set_up.register(Payment, PaymentAdmin)
admin_set_up.register(FeedBack)
admin_set_up.register(CourseRegistration)
admin_set_up.register(AccessModel, AccessModelAdmin)
