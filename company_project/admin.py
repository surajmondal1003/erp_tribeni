from django.contrib import admin
from company_branch.models import CompanyBranch,StorageLocation,UOM,StorageBin

# Register your models here.
admin.site.register(CompanyBranch)
admin.site.register(StorageLocation)
admin.site.register(UOM)
admin.site.register(StorageBin)
