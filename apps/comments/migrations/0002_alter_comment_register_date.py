# Generated by Django 4.2 on 2023-08-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='register_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج'),
        ),
    ]
