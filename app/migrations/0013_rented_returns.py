# Generated by Django 5.0.2 on 2024-03-14 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_books_publisherid'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented',
            name='returns',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
