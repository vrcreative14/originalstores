from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Store)
admin.site.register(StoreCategory)
admin.site.register(StoreSubcategory)
admin.site.register(StoreDetails)
admin.site.register(StoreManager)
admin.site.register(Designation)