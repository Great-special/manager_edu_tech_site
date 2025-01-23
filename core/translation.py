from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Course, Testimonial

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')

class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'duration')    

class TestimonialTranslationOptions(TranslationOptions):
    fields = ('author_name', 'author_title', 'content')


translator.register(Category, CategoryTranslationOptions)
translator.register(Course, CourseTranslationOptions)
translator.register(Testimonial, TestimonialTranslationOptions)