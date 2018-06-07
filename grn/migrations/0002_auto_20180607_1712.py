# Generated by Django 2.0.5 on 2018-06-07 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company_project', '0002_auto_20180607_1214'),
        ('purchase_order', '0001_initial'),
        ('grn', '0001_initial'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grn',
            name='po_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase_order.PurchaseOrder'),
        ),
        migrations.AddField(
            model_name='grn',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company_project.CompanyProject'),
        ),
        migrations.AddField(
            model_name='grn',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.Vendor'),
        ),
        migrations.AddField(
            model_name='grn',
            name='vendor_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.VendorAddress'),
        ),
    ]
