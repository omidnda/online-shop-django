# Generated by Django 4.2 on 2023-07-29 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customuser_forget_password_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره تلفن')),
                ('adress', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'مشتری ها',
            },
        ),
    ]
