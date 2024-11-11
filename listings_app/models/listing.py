from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from listings_app.models.profile import Profile


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    rooms = models.FloatField()
    property_type = models.CharField(max_length=50, choices=[
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField(null=True, blank=True, help_text="Дата начала доступности для аренды")
    available_until = models.DateField(null=True, blank=True, help_text="Дата окончания доступности для аренды")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, primary_key=True)

    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            created_at_value = self.created_at or timezone.now()
            base_slug = slugify(f'{self.title}-{created_at_value.strftime("%Y-%m-%d")}')
            unique_slug = base_slug
            num = 1
            while Listing.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)

    # prepopulated_fields = {"slug" : ("name",)}

    def __str__(self):
        return self.title

    #
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    # def delete(self, *args, **kwargs):
    #     self.is_deleted = True
    #     self.save()
