# Generated by Django 2.0.5 on 2018-06-07 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uom', '0001_initial'),
        ('material_master', '0005_auto_20180607_1244'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GRN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grn_no', models.CharField(max_length=255)),
                ('waybill_no', models.CharField(blank=True, max_length=150, null=True)),
                ('vehicle_no', models.CharField(blank=True, max_length=150, null=True)),
                ('check_post', models.CharField(blank=True, max_length=255, null=True)),
                ('challan_no', models.CharField(max_length=150)),
                ('challan_date', models.DateTimeField()),
                ('is_approve', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('is_finalised', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GRNDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receive_quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('grn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grn_detail', to='grn.GRN')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='material_master.Material')),
                ('uom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='uom.UOM')),
            ],
        ),
        migrations.CreateModel(
            name='ReversGRN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revers_gen_no', models.CharField(max_length=255)),
                ('reverse_quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reverse_reason', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=True)),
                ('is_approve', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('is_finalised', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('grn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grn.GRN')),
            ],
        ),
    ]