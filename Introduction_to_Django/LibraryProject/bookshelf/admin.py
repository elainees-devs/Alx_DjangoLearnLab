from django.contrib import admin
from .models import Book

# Customize how the Book model appears in admin  interface
class BookAdmin(admin.ModelAdmin):
    list_display=("title", "author", "publication_year") # columns to display
    list_filter=("publication_year", "author") #filters on the sidebar
    search_fields=("title", "author")


# Register the model with its custom admin configuration
admin.site.register(Book, BookAdmin)

