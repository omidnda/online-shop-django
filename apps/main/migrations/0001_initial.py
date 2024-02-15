# Generated by Django 4.2 on 2023-08-11 19:06

from django.db import migrations, models
import django.utils.timezone
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_title1', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن اول')),
                ('slider_title2', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن دوم')),
                ('slider_title3', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن سوم')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر اسلاید')),
                ('slider_link', models.URLField(blank=True, null=True, verbose_name='لینک')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='وضعیت')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ به ردز رسانی')),
            ],
            options={
                'verbose_name': 'اسلاید',
                'verbose_name_plural': 'اسلایدها',
            },
        ),
    ]
