from django.db import models
from django.urls import reverse
from listings_app.models.profiles import Profile


class Listing(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='listings')

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.FloatField()
    property_type = models.CharField(max_length=50, choices=[
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=100, null=True)

    # prepopulated_fields = {"slug" : ("name",)}

    def __str__(self):
        return self.title

    #
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    # def delete(self, *args, **kwargs):
    #     self.is_deleted = True
    #     self.save()