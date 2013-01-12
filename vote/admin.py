from django.contrib import admin
from .models import Category, Option

class OptionInline(admin.TabularInline):
    model = Option

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]

admin.site.register(Category, CategoryAdmin)
