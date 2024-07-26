# Generated by Django 5.0 on 2024-06-05 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_blogreview_article"),
    ]

    operations = [
        migrations.CreateModel(
            name="Visitor",
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
                ("ip_address", models.GenericIPAddressField()),
                ("country", models.CharField(max_length=100)),
                ("visit_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="blogreview",
            name="subject",
        ),
    ]
