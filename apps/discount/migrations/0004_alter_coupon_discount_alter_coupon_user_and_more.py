# Generated by Django 4.2 on 2023-07-31 19:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discount', '0003_remove_coupon_customer_coupon_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_coupon', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='discountbasket',
            name='discount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف'),
        ),
    ]
