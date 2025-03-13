# accounts/migrations/0002_auto_set_roles.py

from django.db import migrations

def set_default_roles(apps, schema_editor):
    CustomUser = apps.get_model('account', 'CustomUser')
    for user in CustomUser.objects.all():
        if user.is_superuser:
            user.role = 'admin'
        else:
            user.role = 'employee'
        user.save()

class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_default_roles),
    ]