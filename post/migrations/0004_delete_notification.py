# Generated by Django 5.1.2 on 2025-04-05 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0003_post_salaire"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Notification",
        ),
    ]
