# Generated by Django 4.2 on 2023-07-29 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone_number',
        ),
    ]
