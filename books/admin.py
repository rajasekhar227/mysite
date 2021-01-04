from django.contrib import admin

# Register your models here.
from books.models import books

class booksAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_name', 'author','Book_count')

admin.site.register(books,booksAdmin)