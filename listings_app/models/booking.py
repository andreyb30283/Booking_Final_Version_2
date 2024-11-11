from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .listing import Listing


class Booking(models.Model):
    listing = models.ForeignKey(Listing, to_field='slug', on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)  # Confirmed by landlord
    is_canceled = models.BooleanField(default=False)  # Confirmed by user
    cancel_deadline = models.DateField(null=True, blank=True)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be before thr end date')
        if self.start_date < timezone.now().date():
            raise ValidationError('Start date can not be in the past.')

    def __str__(self):
        return f"{self.listing.title} - {self.user.username}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})
