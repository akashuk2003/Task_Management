from django.db import migrations

def create_admin_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Admin')

class Migration(migrations.Migration):

    dependencies = [
        # This points to the UserProfile migration file you just showed me.
        ('tasks', '0002_userprofile'), 
    ]

    operations = [
        migrations.RunPython(create_admin_group),
    ]