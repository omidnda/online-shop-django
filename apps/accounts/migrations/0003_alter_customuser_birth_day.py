# Generated by Django 4.2 on 2023-05-08 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_mobile_nummber_customuser_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_day',
            field=models.DateField(blank=True),
        ),
    ]