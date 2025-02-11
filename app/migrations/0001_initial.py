# Generated by Django 5.0.2 on 2024-03-02 06:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctgname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=255)),
                ('author_name', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('rent', models.IntegerField()),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('date', models.DateField(auto_now_add=True)),
                ('genere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='bag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.TextField(max_length=255)),
                ('author', models.TextField(max_length=255)),
                ('price', models.TextField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.books')),
                ('genere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(auto_now_add=True)),
                ('to_date', models.DateField(auto_now_add=True)),
                ('total', models.IntegerField()),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.books')),
                ('buser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='rented',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.TextField(max_length=255)),
                ('author', models.TextField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('price', models.TextField(max_length=255)),
                ('fromdate', models.DateField()),
                ('todate', models.DateField()),
                ('total', models.TextField(max_length=255)),
                ('fine', models.TextField(max_length=255)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.books')),
                ('genere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.TextField(max_length=255)),
                ('address', models.TextField(max_length=255)),
                ('phone', models.TextField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
