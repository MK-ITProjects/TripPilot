import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    favorite_destinations = models.ManyToManyField('destinations.Destination', blank=True, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class EmailOTP(models.Model):
    OTP_VALIDITY_MINUTES = 10

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_otp')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OTP for {self.user.username}"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=self.OTP_VALIDITY_MINUTES)

    @classmethod
    def generate_for(cls, user):
        code = f"{secrets.randbelow(1000000):06d}"
        otp, _ = cls.objects.update_or_create(user=user, defaults={'code': code})
        return otp
