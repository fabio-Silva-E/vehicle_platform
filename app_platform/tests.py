from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Car, Manufacturer


class CarTest(TestCase):
    def test_create_car(self):
        user = get_user_model().objects.create(username="test")
        manufacturer = Manufacturer.objects.create(name="BMW", country="DE")

        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
            owner=user,
            year=2022
        )

        self.assertEqual(str(car), "X5")