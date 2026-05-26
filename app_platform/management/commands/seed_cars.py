from decimal import Decimal
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from app_platform.models import Car, Manufacturer, AdPlan, CarImage


class Command(BaseCommand):
    help = "Gera anúncios em massa"

    def handle(self, *args, **options):

        User = get_user_model()

        TOTAL_ANUNCIOS = 1000

        user = User.objects.first()
        if not user:
            raise Exception("Nenhum usuário encontrado.")

        manufacturers_names = [
            "Chevrolet", "Volkswagen", "Fiat", "Ford",
            "Toyota", "Honda", "Hyundai", "BMW",
            "Mercedes", "Audi",
        ]

        manufacturers = []
        for name in manufacturers_names:
            manufacturer, _ = Manufacturer.objects.get_or_create(name=name)
            manufacturers.append(manufacturer)

        plans = list(AdPlan.objects.all())
        if not plans:
            raise Exception("Nenhum plano encontrado.")

        models = [
            "Vectra", "Civic", "Corolla", "Gol", "Palio",
            "Uno", "Cruze", "HB20", "Onix", "Fusion",
            "Hilux", "S10", "Ranger", "Toro", "Compass",
        ]

        categories = ["carro", "equipamento", "animal", "fazenda", "caminhao"]

        image_path = "media/seed/car_default.jpg"

        with open(image_path, "rb") as f:
            image_content = f.read()

        for i in range(TOTAL_ANUNCIOS):

            car = Car(
                owner=user,
                manufacturer=random.choice(manufacturers),
                plan=random.choice(plans),
                category=random.choice(categories),
                model=f"{random.choice(models)} {i}",
                year=random.randint(1990, 2026),
                description=f"Anúncio automático de teste {i}",
                value=Decimal(str(random.uniform(5000, 500000))),
                whatsapp="14999999999",
                is_active=True,
                is_paid=True,
            )

            car.set_expiration()
            car.save()  # precisa do ID

            max_images = car.plan.max_images

            for img_index in range(max_images):
                CarImage.objects.create(
                    car=car,
                    image=ContentFile(
                        image_content,
                        f"car_{i}_{img_index}.jpg"
                    )
                )

            self.stdout.write(f"✅ {i+1} anúncios criados")

        self.stdout.write(
            self.style.SUCCESS(
                f"🔥 FINALIZADO: {TOTAL_ANUNCIOS} anúncios criados."
            )
        )