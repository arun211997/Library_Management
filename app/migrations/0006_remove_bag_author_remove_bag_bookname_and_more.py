# Generated by Django 5.0.2 on 2024-03-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_purchase_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bag',
            name='author',
        ),
        migrations.RemoveField(
            model_name='bag',
            name='bookname',
        ),
        migrations.RemoveField(
            model_name='bag',
            name='genere',
        ),
        migrations.RemoveField(
            model_name='bag',
            name='image',
        ),
        migrations.RemoveField(
            model_name='bag',
            name='price',
        ),
        migrations.AddField(
            model_name='bag',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
