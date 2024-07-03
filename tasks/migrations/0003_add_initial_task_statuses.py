from django.db import migrations


def create_initial_statuses(apps, schema_editor):
    TaskStatus = apps.get_model('tasks', 'TaskStatus')
    TaskStatus.objects.bulk_create([
        TaskStatus(name='not_started'),
        TaskStatus(name='in_progress'),
        TaskStatus(name='completed')
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
        ('tasks', '0002_taskstatus_task_status')
    ]

    operations = [
        migrations.RunPython(create_initial_statuses),
    ]
