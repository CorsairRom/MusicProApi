from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class MyAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Realiza cualquier configuración necesaria para tus pruebas

    def test_my_api_view(self):
        url = '/api/producto/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Realiza más aserciones para verificar el comportamiento esperado
