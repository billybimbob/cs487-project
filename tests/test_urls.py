from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import home, signup, account_info, account_spots, account_payments


class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('accounts:home')
        self.assertEquals(resolve(url).func, home)

    def test_signup_url(self):
        url = reverse('accounts:signup')
        self.assertEquals(resolve(url).func, signup)

    def test_account_info_url(self):
        url = reverse('accounts:account-info')
        self.assertEquals(resolve(url).func, account_info)
    
    def test_account_spot_url(self):
        url = reverse('accounts:account-spots')
        self.assertEquals(resolve(url).func, account_spots)

    def test_account_payment_url(self):
        url = reverse('accounts:account-payments')
        self.assertEquals(resolve(url).func, account_payments)