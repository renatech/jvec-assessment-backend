from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Contacts


# Create your tests here.
class ContactViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_all_contacts(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_contact(self):
        contact = Contacts.objects.create(first_name='John', last_name='Doe', phone_number='123456789')
        response = self.client.get(f'/contact/{contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact(self):
        data = {'first_name': 'Jane', 'last_name': 'Doe', 'phone_number': '987654321'}
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_contact(self):
        contact = Contacts.objects.create(first_name='John', last_name='Doe', phone_number='123456789')
        data = {'first_name': 'Updated', 'last_name': 'Doe', 'phone_number': '987654321'}
        response = self.client.put(f'/contact/{contact.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contact(self):
        contact = Contacts.objects.create(first_name='John', last_name='Doe', phone_number='123456789')
        response = self.client.delete(f'/contact/{contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
