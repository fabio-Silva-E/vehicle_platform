from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ApprovePaymentView,
    CarCreateView,
    CarDeleteView,
    CarDetailView,
    CarListView,
    CarUpdateView,
    DeleteCarImageView,
    FavoriteListView,
    MyCarsView,
    PaymentView,
    RegisterView,
    ToggleFavoriteView,
)
from .webhooks import asaas_webhook

urlpatterns = [
    path("", CarListView.as_view(), name="car-list"),
    path("car/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("car/create/", CarCreateView.as_view(), name="car-create"),
    path("register/", RegisterView.as_view(), name="register"),
    path("car/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("car/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path("image/<int:pk>/delete/",
         DeleteCarImageView.as_view(), name="image-delete"),
    path("payment/<int:pk>/", PaymentView.as_view(), name="payment"),
    path(
        "approve-payment/<int:pk>/",
        ApprovePaymentView.as_view(),
        name="approve-payment",
    ),
    path("meus-anuncios/", MyCarsView.as_view(), name="my-cars"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("favorites/", FavoriteListView.as_view(), name="favorite-list"),
    path("favorite/<int:pk>/", ToggleFavoriteView.as_view(), name="toggle-favorite"),
    path("webhooks/asaas/", asaas_webhook, name="asaas-webhook"),
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

app_name = "platform"
