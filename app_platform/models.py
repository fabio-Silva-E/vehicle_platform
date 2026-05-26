from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class AdPlan(models.Model):

    PLAN_CHOICES = [
        ("basico", "Básico"),
        ("premium", "Premium"),
        ("destaque", "Destaque"),
    ]

    name = models.CharField(
        "Plano",
        max_length=20,
        choices=PLAN_CHOICES,
        unique=True
    )

    price = models.DecimalField(
        "Preço",
        max_digits=10,
        decimal_places=2,
        default=0
    )

    max_images = models.PositiveIntegerField(
        "Máximo de imagens",
        default=4
    )

    duration_days = models.PositiveIntegerField(
        "Duração em dias",
        default=7
    )

    priority = models.PositiveIntegerField(
        "Prioridade",
        default=3
    )

    class Meta:
        verbose_name = "Plano de anúncio"
        verbose_name_plural = "Planos de anúncios"
        ordering = ["priority"]

    # 🔥 TIPOS DE PLANO

    def is_basico(self):
        return self.name == "basico"

    def is_premium(self):
        return self.name == "premium"

    def is_destaque(self):
        return self.name == "destaque"

    # 🔥 BADGE VISUAL

    @property
    def badge(self):

        badges = {
            "basico": "🟢 Básico",
            "premium": "⭐ Premium",
            "destaque": "🔥 Destaque",
        }

        return badges.get(
            self.name,
            self.get_name_display()
        )

    # 🔥 CSS CLASS

    @property
    def css_class(self):
        return self.name

    # 🔥 FORMATAÇÃO DE PREÇO

    @property
    def formatted_price(self):
        return f"R$ {self.price:.2f}"

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    cpf_cnpj = models.CharField(
            max_length=18,
            blank=True
        )
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

    category = models.CharField(
        "Categoria",
        max_length=255,
        choices=CATEGORY_CHOICES,
        default="carro"
    )

    plan = models.ForeignKey(
        "AdPlan",
        on_delete=models.PROTECT,
        related_name="cars"
    )

    is_paid = models.BooleanField(default=False)

    expires_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)

    model = models.CharField(
        "Modelo",
        max_length=255,
        blank=True,
        null=True
    )

    manufacturer = models.ForeignKey(
        "Manufacturer",
        verbose_name="Fabricante",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    year = models.IntegerField("Ano", null=True, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Dono",
        on_delete=models.CASCADE
    )

    description = models.TextField("Descrição", blank=True)

    value = models.DecimalField(
        "Valor",
        max_digits=15,
        decimal_places=2,
        default=0
    )

    whatsapp = models.CharField(
        "WhatsApp",
        max_length=20,
        blank=True
    )

    def max_images(self):
        return self.plan.max_images

    def priority(self):
        return self.plan.priority

    def is_premium(self):
        return self.plan.is_premium()

    def is_destaque(self):
        return self.plan.is_destaque()

    def set_expiration(self):
        self.expires_at = (
            timezone.now() +
            timedelta(days=self.plan.duration_days)
        )

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

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "car")

        verbose_name = "Ver Depois"
        verbose_name_plural = "Ver Depois"

    def __str__(self):
        return f"{self.user} -> {self.car}"


class Payment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("paid", "Pago"),
        ("expired", "Expirado"),
    ]

    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE
    )

    payment_id = models.CharField(
        max_length=255
    )

    invoice_url = models.URLField()

    pix_code = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

