# Generated by Django 4.2 on 2023-07-30 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_customer_phone_number'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_coupon', to='accounts.customer', verbose_name='مشتری'),
        ),
    ]