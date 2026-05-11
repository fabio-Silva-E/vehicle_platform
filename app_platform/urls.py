from django.urls import path
from .views import (CarListView,
                    RegisterView,
                    CarCreateView,
                    CarUpdateView,
                    CarDeleteView,
                    CarDetailView,
                    DeleteCarImageView, PaymentView, ApprovePaymentView, MyCarsView
                    )
urlpatterns = [
    path("", CarListView.as_view(), name="car-list"),
    path("car/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("car/create/", CarCreateView.as_view(), name="car-create"),
    path("register/", RegisterView.as_view(), name="register"),
    path("car/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("car/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path("image/<int:pk>/delete/", DeleteCarImageView.as_view(), name="image-delete"),
    path(
        "payment/<int:pk>/",
        PaymentView.as_view(),
        name="payment"
    ),
    path(
           "approve-payment/<int:pk>/",
           ApprovePaymentView.as_view(),
           name="approve-payment"
       ),
path(
    "meus-anuncios/",
    MyCarsView.as_view(),
    name="my-cars"
),

]

app_name = "platform"