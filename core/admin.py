from django.contrib import admin
from .models import Category, Course, Testimonials
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)