# Generated by Django 2.0.5 on 2018-06-08 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material_master', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('states', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('project_address', models.CharField(blank=True, max_length=100, null=True)),
                ('project_city', models.CharField(blank=True, max_length=100, null=True)),
                ('project_pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('project_contact_no', models.BigIntegerField(blank=True, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=100, null=True)),
                ('project_gstin', models.CharField(blank=True, max_length=50, null=True)),
                ('engineer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('engineer_contact_no', models.BigIntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_approve', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('is_finalised', models.CharField(choices=[('2', 'False'), ('1', 'True'), ('0', 'None')], default='0', max_length=1)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_project', to='company.Company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='states.State')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProjectDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('boq_ref', models.CharField(blank=True, max_length=50, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('avail_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='material_master.Material')),
                ('materialtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='material_master.MaterialType')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_details', to='company_project.CompanyProject')),
            ],
        ),
    ]
