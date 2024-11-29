# Generated by Django 5.1 on 2024-11-28 19:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("username", models.CharField(max_length=128, unique=True)),
                ("position", models.CharField(max_length=128)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Advertisement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        default="product.svg", upload_to="advertisement/"
                    ),
                ),
                ("category", models.CharField(default="", max_length=128)),
                ("sns", models.CharField(default="", max_length=128)),
                ("title", models.CharField(max_length=128)),
                ("product_name", models.CharField(max_length=128)),
                ("description", models.TextField(default="description of the product")),
                ("min_budget", models.PositiveIntegerField(default=0)),
                ("max_budget", models.PositiveIntegerField(default=0)),
                (
                    "product_image",
                    models.ImageField(
                        default="product.svg", upload_to="advertisement/"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="advertisements",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("img", models.ImageField(default="product.svg", upload_to="profile/")),
                ("platform", models.CharField(default="", max_length=128)),
                ("content", models.CharField(default="", max_length=128)),
                ("min_budget", models.PositiveIntegerField(default=0)),
                ("max_budget", models.PositiveIntegerField(default=0)),
                ("urls", models.CharField(default="", max_length=100)),
                ("text_box", models.CharField(default="", max_length=512)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]