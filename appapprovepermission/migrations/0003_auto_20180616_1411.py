# Generated by Django 2.0.5 on 2018-06-16 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appapprovepermission', '0002_auto_20180616_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empapprovedetail',
            name='emp_approve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp_approve_details', to='appapprovepermission.EmpApprove'),
        ),
    ]