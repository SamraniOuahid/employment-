# Generated by Django 5.1.2 on 2025-04-10 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0010_remove_post_accepted_postapplication_step_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="InterviewResponse",
        ),
    ]
