from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        customer = Customer()
        customer.save()
        user.customer = customer

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Customer(models.Model): # for tracking payments
    cid = models.AutoField(primary_key=True)

    def __str__(self):
        return f'customer {self.cid}'


class User(AbstractUser): # an account
    """User model."""
    username = None
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    email    = models.EmailField(ugettext_lazy('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'user {self.email}'


def after30days():
    return timezone.now() + timedelta(days=30)
    
class Member(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)    
    start_date = models.DateField(auto_now_add=True)
    end_date   = models.DateField(default=after30days)

    def __str__(self):
        return f'member of {self.user}'

