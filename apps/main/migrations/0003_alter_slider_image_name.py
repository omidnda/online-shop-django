# Generated by Django 4.2 on 2023-08-15 19:48

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_slider_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر اسلاید'),
        ),
    ]
