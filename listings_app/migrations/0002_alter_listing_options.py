# Generated by Django 5.1.2 on 2024-11-12 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listing',
            options={'ordering': ['-created_at']},
        ),
    ]