# Generated by Django 5.0.2 on 2024-05-10 21:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalApp', '0007_alter_semestersubject_teachers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semestersubject',
            name='Teachers',
        ),
        migrations.CreateModel(
            name='teacher_subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalApp.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalApp.teacher')),
            ],
        ),
    ]
