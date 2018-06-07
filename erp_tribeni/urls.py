"""ERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from rest_framework import routers
from authentication import views
from states import views
# from company import views
# from company_branch import views
# from purchaseorggroup import views
# from salesorg_group import views
# from material_master import views
# from purchase_requisition import views
# from gstrates import views
# from transporter import views
# from vendor import views
from banks import views
# from purchase_order import views
# from grn import views
# from purchase_invoice import views
# from payment import views
# from stock import views
# from departments import views
# from designation import views
# from employee import views
# from contractor import views
from company_project import views


urlpatterns = [

    path('', include('authentication.urls')),
    path('', include('states.urls')),
    path('', include('company.urls')),
    # path('', include('company_branch.urls')),
    # path('', include('purchaseorggroup.urls')),
    # path('', include('salesorg_group.urls')),
    path('', include('material_master.urls')),
    path('', include('purchase_requisition.urls')),
    path('', include('gstrates.urls')),
    path('', include('transporter.urls')),
    path('', include('vendor.urls')),
    path('', include('banks.urls')),
    # path('', include('purchase_order.urls')),
    # path('', include('grn.urls')),
    # path('', include('purchase_invoice.urls')),
    # path('', include('payment.urls')),
    # path('', include('stock.urls')),
    path('', include('departments.urls')),
    path('', include('designation.urls')),
    # path('', include('employee.urls')),
    path('', include('contractor.urls')),
    path('', include('uom.urls')),
    path('', include('company_project.urls')),
    path('admin/', admin.site.urls),
]
