from django.contrib import admin

from .models import Watch, WatchOption

class WatchOptionInline(admin.TabularInline):
    model = WatchOption
    max_num = 2
    extra = 2

class WatchAdmin(admin.ModelAdmin):
    inlines = [
        WatchOptionInline,
    ]

admin.site.register(Watch, WatchAdmin)
