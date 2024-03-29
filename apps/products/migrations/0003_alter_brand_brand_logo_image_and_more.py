# Generated by Django 4.2 on 2023-07-08 18:46

from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_brand_brand_logo_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_logo_image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر برند کالا'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_of_brands', to='products.brand', verbose_name='برند کالا'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا'),
        ),
        migrations.AlterField(
            model_name='productimagegallery',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
    ]
