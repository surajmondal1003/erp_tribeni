# Generated by Django 2.0.5 on 2018-06-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0003_remove_purchaseorderdetail_material_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderdetail',
            name='avail_qty',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
