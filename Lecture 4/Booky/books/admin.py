from django.contrib import admin
from .models import Book, BookReader, Person

# Register your models here.
admin.site.register(Book)
admin.site.register(BookReader)
admin.site.register(Person)
