# Generated by Django 2.0.5 on 2018-06-12 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_requisition', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisitiondetail',
            name='avail_qty',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
