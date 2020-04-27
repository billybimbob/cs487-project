from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Customer, Member
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')

#    def test_signup_view(self):
#        response = self.client.get(reverse)

#    def test_account_info_view(self):
#        response = self.client.get(reverse)

#    def test_account_spots_view(self):
#        response = self.client.get(reverse)

#    def test_account_payments_view(self):
#        response = self.client.get(reverse)