from django.contrib import admin
from .models import Car, CarImage, Manufacturer
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "phone", "city", "is_staff")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ("phone", "city"),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Informações adicionais", {
            "fields": ("phone", "city"),
        }),
    )

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "manufacturer", "year", "owner")
    search_fields = ("model", "manufacturer__name")
    list_filter = ("manufacturer", "year")
    inlines = [CarImageInline]


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ("name",)

from django.utils.html import format_html

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return ""