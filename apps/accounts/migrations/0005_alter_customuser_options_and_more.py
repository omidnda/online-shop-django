# Generated by Django 4.2 on 2023-05-08 20:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_birth_day'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='active_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='کد فعال سازی'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='birth_day',
            field=models.DateField(blank=True, null=True, verbose_name='زادروز'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=200, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='family',
            field=models.CharField(blank=True, max_length=20, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('1', 'مرد'), ('2', 'زن'), ('3', 'دیگر')], default='1', max_length=5, null=True, verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='مدیر سایت'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=20, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='گدرواژه'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='register_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ثبت'),
        ),
    ]
