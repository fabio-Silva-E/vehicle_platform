from django.contrib import admin

from .models import (
    User,
    Manufacturer,
    Car,
    CarImage,
    Listing,
    Favorite,
    Payment,
    AdPlan
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "cpf_cnpj",
        "city",
        "is_staff"
    )

    search_fields = (
        "username",
        "email",
        "cpf_cnpj"
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        "model",
        "category",
        "plan",
        "owner",
        "value",
        "is_paid",
        "is_active",
        "expires_at"
    )

    list_filter = (
        "category",
        "is_paid",
        "is_active",
        "plan"
    )

    search_fields = (
        "model",
        "owner__username"
    )

    inlines = [CarImageInline]


@admin.register(AdPlan)
class AdPlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "max_images",
        "duration_days",
        "priority"
    )


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):

    list_display = (
        "car",
        "type",
        "price",
        "is_available"
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "car",
        "created_at"
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "car",
        "payment_id",
        "status",
        "created_at"
    )

    list_filter = ("status",)

    search_fields = (
        "payment_id",
        "car__model"
    )