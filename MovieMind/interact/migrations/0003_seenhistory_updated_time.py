# Generated by Django 5.2 on 2025-04-26 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interact", "0002_comment_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="seenhistory",
            name="updated_time",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
