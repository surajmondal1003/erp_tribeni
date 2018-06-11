from django.db import models
from django.contrib.auth.models import User
from uom.models import UOM


# Create your models here.

class MaterialType(models.Model):
    material_type=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.material_type)

    def material_type_id(self):
        return self.id

    def material_type_name(self):
        return self.material_type


class Material(models.Model):
    material_fullname=models.CharField(max_length=100)
    material_type=models.ForeignKey(MaterialType,on_delete=models.SET_NULL,blank=True,null=True)
    material_code=models.CharField(max_length=25)
    description=models.TextField()
    is_taxable=models.BooleanField(default=False)
    is_sales=models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    margin = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.material_fullname)



class Material_UOM(models.Model):
    MATERIAL_CHOICES = (
        ('1', 'Purchase'),
        ('2', 'Sales'),
    )


    material=models.ForeignKey(Material,on_delete=models.CASCADE,related_name='material_uom')
    material_for=models.CharField(max_length=1,choices=MATERIAL_CHOICES,default='1')
    base_uom=models.ForeignKey(UOM,on_delete=models.SET_NULL,blank=True,null=True,related_name='base_uom')
    unit_per_uom=models.DecimalField(max_digits=10,decimal_places=2 , blank=True,null=True)
    unit_uom=models.ForeignKey(UOM,on_delete=models.SET_NULL,blank=True,null=True,related_name='unit_uom')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.material.material_fullname)


class Material_Tax(models.Model):
    TAX_CHOICES = (
        ('1', 'Purchase'),
        ('2', 'Sales'),
    )

    material = models.ForeignKey(Material, on_delete=models.CASCADE,related_name='material_tax')
    tax_for = models.CharField(max_length=1, choices=TAX_CHOICES, default='1')
    igst=models.DecimalField(max_digits=10,decimal_places=2)
    cgst=models.DecimalField(max_digits=10,decimal_places=2)
    sgst=models.DecimalField(max_digits=10,decimal_places=2)
    hsn=models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return str(self.material.material_fullname)





