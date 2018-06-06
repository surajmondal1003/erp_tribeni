from django.contrib import admin
from material_master.models import Material_Tax,Material_UOM,Material,MaterialType

# Register your models here.
admin.site.register(Material)
admin.site.register(Material_Tax)
admin.site.register(Material_UOM)
admin.site.register(MaterialType)
