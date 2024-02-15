# Generated by Django 4.2 on 2023-08-07 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0019_alter_brand_brand_logo_image_and_more'),
        ('scoring_favorite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_product', to='products.product', verbose_name='کالا')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to=settings.AUTH_USER_MODEL, verbose_name='کاربر علاقه مند')),
            ],
            options={
                'verbose_name': 'علاقه مندی',
                'verbose_name_plural': 'علاقه مندی ها',
            },
        ),
    ]
