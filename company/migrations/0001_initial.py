# Generated by Django 2.0.5 on 2018-06-08 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('states', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('company_url', models.CharField(blank=True, max_length=255, null=True)),
                ('company_gst', models.CharField(blank=True, max_length=50, null=True)),
                ('company_pan', models.CharField(blank=True, max_length=50, null=True)),
                ('company_cin', models.CharField(blank=True, max_length=50, null=True)),
                ('company_email', models.EmailField(blank=True, max_length=50, null=True)),
                ('company_address', models.CharField(max_length=100)),
                ('company_contact', models.BigIntegerField()),
                ('company_city', models.CharField(max_length=100)),
                ('company_pin', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('company_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='states.State')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='company.Company')),
            ],
        ),
        migrations.CreateModel(
            name='TermsandConditon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_type', models.CharField(blank=True, choices=[('1', 'Purchase'), ('2', 'Sales'), ('3', 'Payment'), ('4', 'Delivery'), ('5', 'Others')], default=None, max_length=1, null=True)),
                ('term_text', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
