# Generated by Django 5.0.2 on 2024-05-11 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalApp', '0008_remove_semestersubject_teachers_teacher_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher_subject',
            name='Subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalApp.semestersubject'),
        ),
    ]