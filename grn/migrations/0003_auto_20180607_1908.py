# Generated by Django 2.0.5 on 2018-06-07 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grn', '0002_auto_20180607_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reversgrn',
            name='grn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reverse_grn', to='grn.GRN'),
        ),
    ]
