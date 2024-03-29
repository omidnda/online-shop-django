# Generated by Django 4.2 on 2023-08-02 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0014_alter_brand_brand_logo_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehauseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ware_hause_type_title', models.CharField(max_length=50, verbose_name='نوع انبار')),
            ],
            options={
                'verbose_name': 'نوع انبار',
                'verbose_name_plural': 'انواع روش انبار',
            },
        ),
        migrations.CreateModel(
            name='Warehause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='تعداد')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='قیمت واحد')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehause_products', to='products.product', verbose_name='کالا')),
                ('user_registered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehauseuser_registered', to=settings.AUTH_USER_MODEL, verbose_name='کاربر انباردار')),
                ('warehaus_taype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehauses', to='warehauses.warehausetype', verbose_name='انبار')),
            ],
            options={
                'verbose_name': 'انبار',
                'verbose_name_plural': 'انبارها',
            },
        ),
    ]
