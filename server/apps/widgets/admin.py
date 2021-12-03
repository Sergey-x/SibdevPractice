from django.contrib import admin

from .models.widget import Widget


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    pass
