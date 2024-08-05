# Generated by Django 5.0.2 on 2024-06-06 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalApp', '0019_dm_notification_title_alter_dm_notification_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='published',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DepartmentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published', to='FinalApp.department')),
            ],
        ),
    ]