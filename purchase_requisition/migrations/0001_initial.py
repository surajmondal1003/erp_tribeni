# Generated by Django 2.0.5 on 2018-06-08 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material_master', '0001_initial'),
        ('uom', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('company_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisition_no', models.CharField(max_length=255)),
                ('special_note', models.TextField()),
                ('is_approve', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('is_finalised', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisition_company', to='company.Company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisition_by', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company_project.CompanyProject')),
            ],
        ),
        migrations.CreateModel(
            name='RequisitionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=True)),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='material_master.Material')),
                ('material_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material_master.MaterialType')),
                ('requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisition_detail', to='purchase_requisition.Requisition')),
                ('uom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='uom.UOM')),
            ],
        ),
    ]
