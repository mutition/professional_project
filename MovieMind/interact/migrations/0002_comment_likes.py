# Generated by Django 5.2 on 2025-04-26 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interact", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="likes",
            field=models.IntegerField(default=0),
        ),
    ]
