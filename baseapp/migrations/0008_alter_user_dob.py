# Generated by Django 5.0.2 on 2024-03-26 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0007_remove_animal_user_identifier_alter_animal_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
