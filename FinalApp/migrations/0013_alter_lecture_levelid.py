# Generated by Django 5.0.2 on 2024-05-22 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalApp', '0012_alter_account_password_alter_subject_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='LevelId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Lectures', to='FinalApp.level'),
        ),
    ]