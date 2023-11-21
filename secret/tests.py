from django.test import TestCase
from .models import Secret


class SecretTests(TestCase):
    def setUp(self):
        self.default = Secret.objects.create(secret="test", passphrase="testpass123123123")
        self.secret = {"passphrase": 'testpass123123123', "secret": 'test'}

    def test_index(self):
        url = 'http://127.0.0.1:8000/'
        response =  self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # SecretViewSet
    def test_create_secret(self):
        url = 'http://127.0.0.1:8000/generate/'
        response = self.client.post(url, self.secret)
        self.assertEqual(response.status_code, 201)

    # SecretPassphraseDetailView
    def test_get_secret_key(self):
        obj = self.default
        url = f'http://127.0.0.1:8000/secrets/secret-key/{obj.generated_key}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # SecretKeyDetailView
    def test_get_key(self):
        url = f'http://127.0.0.1:8000/secrets/{self.secret["passphrase"]}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
