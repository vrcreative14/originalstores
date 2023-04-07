from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(Article)
admin.site.register(ArticleDetails)
admin.site.register(GarmentDetails)
admin.site.register(GarmentSubcategory)
admin.site.register(ProductSubCategory)
admin.site.register(GarmentClassification)
#admin.site.register(ProductType)
admin.site.register(ProductIdentity)
#admin.site.register(HomeDecor)
admin.site.register(HomeDecorDetails)
#admin.site.register(KitchenItem)
admin.site.register(KitchenItemDetails)
#admin.site.register(SportsFitnessEquipment)
admin.site.register(SportsFitnessEquipmentDetails)
#admin.site.register(StationeryItem)
admin.site.register(StationeryItemDetails)
#admin.site.register(HomeAppliance)
admin.site.register(HomeApplianceDetails)