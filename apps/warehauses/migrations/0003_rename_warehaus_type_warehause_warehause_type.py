# Generated by Django 4.2 on 2023-08-02 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehauses', '0002_rename_warehaus_taype_warehause_warehaus_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warehause',
            old_name='warehaus_type',
            new_name='warehause_type',
        ),
    ]
