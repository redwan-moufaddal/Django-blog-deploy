# Generated by Django 5.0 on 2024-06-05 20:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0005_delete_visitor_blogreview_subject"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogreview",
            name="subject",
        ),
    ]
