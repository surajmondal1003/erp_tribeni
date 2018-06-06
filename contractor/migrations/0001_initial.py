# Generated by Django 2.0.5 on 2018-06-06 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('states', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractor_name', models.CharField(max_length=100)),
                ('pan_no', models.CharField(blank=True, max_length=255, null=True)),
                ('gst_no', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=255)),
                ('mobile', models.BigIntegerField()),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='states.State')),
            ],
        ),
        migrations.CreateModel(
            name='ContractorAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=255)),
                ('branch_name', models.CharField(max_length=255)),
                ('account_no', models.CharField(max_length=255)),
                ('ifsc_code', models.CharField(max_length=255)),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor_account', to='contractor.Contractor')),
            ],
        ),
    ]
