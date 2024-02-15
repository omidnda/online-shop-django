# Generated by Django 4.2 on 2023-08-03 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0010_remove_customer_phone_number'),
        ('products', '0017_alter_brand_brand_logo_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='متن نظر')),
                ('register_date', models.DateTimeField(verbose_name='تاریخ درج')),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('comment_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_child', to='comments.comment', verbose_name='والد نظر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_product', to='products.product', verbose_name='کالا')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_user1', to='accounts.customer', verbose_name='کاربر نظر دهنده')),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_user2', to='accounts.customer', verbose_name='کاربر تایید یا رد کننده نظر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
    ]