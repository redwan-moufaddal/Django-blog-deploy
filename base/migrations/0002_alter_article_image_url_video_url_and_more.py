# Generated by Django 5.0 on 2024-05-14 19:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="image_url_video_url",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="article",
            name="keywords",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="article",
            name="title",
            field=models.TextField(),
        ),
    ]
