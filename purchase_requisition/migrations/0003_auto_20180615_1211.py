# Generated by Django 2.0.5 on 2018-06-15 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_requisition', '0002_requisitiondetail_avail_qty'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requisition',
            options={'permissions': (('can_approve', 'Can Approve'),)},
        ),
    ]
