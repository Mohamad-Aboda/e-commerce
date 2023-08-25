from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from .utils import customer_directory_path
User = get_user_model()

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=customer_directory_path, null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


