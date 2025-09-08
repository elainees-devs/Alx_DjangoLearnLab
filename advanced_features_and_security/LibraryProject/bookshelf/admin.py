from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Book

# Customize how the Book model appears in admin  interface
class BookAdmin(admin.ModelAdmin):
    list_display=("title", "author", "publication_year") # columns to display
    list_filter=("publication_year", "author") #filters on the sidebar
    search_fields=("title", "author")


class CustomUserAdmin(UserAdmin):
    """
    Extends Django's built-in UserAdmin to display custom fields.
    """
    model = CustomUser
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )


# Register the model with its custom admin configuration
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

