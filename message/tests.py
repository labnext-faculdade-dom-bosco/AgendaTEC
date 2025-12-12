from django.test import TestCase
from .services import WahaService
import requests


class WahaServiceTestCase(TestCase):
    def setUp(self):
        self.service = WahaService()
        self.phone_number = ""  # Número que vai receber a mensagem. Ex.: 5551xxxxxxxx
        self.message = "Olá, Você recebeu uma mensagem de teste!"

    def test_send_message(self):
        self.assertTrue(self.phone_number)
        self.assertTrue(self.message)

        return self.service.send_message(
            phone_number=self.phone_number,
            message=self.message
        )
