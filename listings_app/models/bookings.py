# from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings

from .listings import Listing


class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)  # Подтверждено арендодателем

    def __str__(self):
        return f"{self.listing.title} - {self.user.username}"


    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


