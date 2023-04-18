# Generated by Django 4.2 on 2023-04-16 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Interest",
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
                ("name", models.CharField(max_length=50)),
            ],
        ),
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
                ("full_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=20, unique=True)),
                ("gender", models.CharField(max_length=10)),
                ("country", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=100)),
                ("is_online", models.BooleanField(default=False)),
                ("interests", models.ManyToManyField(to="chat.interest")),
            ],
        ),
    ]