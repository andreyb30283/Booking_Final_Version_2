
from django.db import models
from django.urls import reverse
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_landlord = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})