# Generated by Django 5.0.2 on 2024-03-26 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0004_alter_animal_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='uploaded_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='animal',
            old_name='uploaded_by_identifier',
            new_name='user_identifier',
        ),
    ]