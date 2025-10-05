from django.contrib import admin

from app_name.models import Pizza


# Register your models here.


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    pass
