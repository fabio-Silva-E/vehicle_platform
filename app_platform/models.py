from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Car(models.Model):
    CATEGORY_CHOICES = [
        ("carro", "Carros"),
        ("equipamento", "Equipamentos Pesados"),
        ("animal", "Animais"),
        ("fazenda", "Fazenda"),
        ("caminhao", "Caminhao"),
    ]
    PLAN_CHOICES = [
        ("basico", "Básico"),
        ("premium", "Premium"),
        ("destaque", "Destaque"),
    ]
    category = models.CharField(
        "Categoria",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="carro"
    )
    is_paid = models.BooleanField(default=False)

    expires_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="basico"
    )
    model = models.CharField("Modelo", max_length=255, blank=True,  null=True)

    manufacturer = models.ForeignKey(
        "Manufacturer",
        verbose_name="Fabricante",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    year = models.IntegerField("Ano", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Dono", on_delete=models.CASCADE)


    description = models.TextField("Descrição", blank=True)
    value = models.DecimalField(
        "Valor",
        max_digits=10,
        decimal_places=2,
        default=0
    )
    whatsapp = models.CharField("WhatsApp", max_length=20, blank=True)

    def max_images(self):

        if self.plan == "basico":
            return 4

        elif self.plan == "premium":
            return 15

        elif self.plan == "destaque":
            return 30

        return 4

    def is_premium(self):
        return self.plan == "premium"

    def is_destaque(self):
        return self.plan == "destaque"

    def priority(self):

        if self.plan == "destaque":
            return 1

        elif self.plan == "premium":
            return 2

        return 3

    def set_expiration(self):
        if self.plan == "basico":
            self.expires_at = timezone.now() + timedelta(minutes=10)
        elif self.plan == "premium":
            self.expires_at = timezone.now() + timedelta(days=30)
        elif self.plan == "destaque":
            self.expires_at = timezone.now() + timedelta(days=60)

        return 4
    def __str__(self):
        return self.model


class CarImage(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/")

    def __str__(self):
        return f"Imagem de {self.car.model}"


class Listing(models.Model):
    TYPE_CHOICES = [
        ("sale", "Venda"),
        ("rent", "Aluguel"),
    ]

    car = models.ForeignKey(Car, verbose_name="Carro", on_delete=models.CASCADE)
    type = models.CharField("Tipo", max_length=10, choices=TYPE_CHOICES)

    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    is_available = models.BooleanField("Disponível", default=True)

    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.type}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "car")

