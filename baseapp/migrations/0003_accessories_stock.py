# Generated by Django 5.0.2 on 2024-03-20 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_animal_approved_accessories'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessories',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]