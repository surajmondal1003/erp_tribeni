# Generated by Django 2.0.5 on 2018-06-07 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_master', '0002_materialtype_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material_uom',
            name='unit_per_uom',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
