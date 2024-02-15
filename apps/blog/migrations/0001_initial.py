# Generated by Django 4.2 on 2023-08-15 19:48

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت')),
            ],
            options={
                'verbose_name': 'خبرنامه',
                'verbose_name_plural': 'خبرنامه ها',
            },
        ),
    ]