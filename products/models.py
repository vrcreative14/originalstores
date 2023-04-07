from django.db import models
from multiselectfield import MultiSelectField
from stores.models import Store
from app_global.validator import check_thumbnail,check_detailed_image
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
import qrcode
import random
import os
from io import BytesIO
from accounts.models import Seller
import base64
# Create your models here.

file_path = ''
def get_upload_path(self, name):
        #seller_id = request.session['seller']
        # if seller_id:
        #         seller_name = Seller.objects.filter(seller = seller_id)
        #         seller_name = seller_name + seller_id
        #         return os.path.join("static/images/products/seller_%d/category_%d" %seller_name ,self.product_class,name)
        # else: 
                file_path = os.path.join("static/images/products/store_%s" %self.store.all().first().store_id,name)
                path_folders = file_path.split("\\")
                if os.path.exists(file_path):
                    file_path = path_folders[0] + "/" + path_folders[1] + "/" + name
                
                    #file_path = os.path.join("static/images/products/store_%s" %self.store.all().first().store_id,"product_%s" %self.slug_field,name)
                return file_path


class ProductCategory(models.Model):
       id = models.IntegerField(primary_key=True)
       name = models.CharField(max_length=50, unique=True)

       class Meta:
           verbose_name_plural = 'ProductCategories'

       def __str__(self):
           return self.name

class ProductSubCategory(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    def __str__(self):
            return str(self.name)

class ProductIdentity(models.Model):
    type = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


quantity_unit = [
    ('Pieces','Pieces'),
    ('Dozen','Dozen'),
    ('Kg','Kilogram'),
    ('L','Litre'),
    ('G','Gram'),
    ('M','Metre')
]


def make_thumbnail(self):    
        THUMB_SIZE = (300,350)
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()
        #slug_str = "%s" % (thumb_name) 
        #slug_str = slugify(slug_str) + str(random.randint(9, 99)) + thumb_extension
        #thumb_filename = thumb_name + '_thumb' + thumb_extension
        thumb_filename = get_file_name(self.image.name,"_thumb",self.slug_field)

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type
        
        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image = image.convert('RGB')
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        #image_path = self.image_thumbnail.url
        if os.path.exists(thumb_filename):
            os.remove(thumb_filename)
        self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        #self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()

        return True



class Product(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(validators=[check_thumbnail],upload_to=get_upload_path, height_field=None, blank=True, null=True)
    #image_front = models.ImageField(validators=[check_detailed_image],upload_to='static/images', height_field=None, blank=True)
    image_rear = models.ImageField(upload_to=get_upload_path, height_field=None, blank=True, null=True)
    image_side1 = models.ImageField(upload_to=get_upload_path, height_field=None, blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to=get_upload_path, height_field=None, blank=True, null=True)
    #image_thumbnail = models.CharField(max_length=4000,blank=True, null=True)
    #store=models.ManyToManyField(Store)
    #type=models.ForeignKey(ProductType, on_delete=models.CASCADE)        
    img_path = models.CharField(max_length=100, blank=True)    
    brand_name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    qrcode_text = models.CharField(max_length=250, blank=True, null=True)
    product_id = models.CharField(max_length=50,blank=True, null=True)
    slug_field = models.SlugField(max_length=100, unique=True)
    #product_details = models.ForeignKey(ProductDetails, on_delete=models.SET_DEFAULT)
    #product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    store = models.ManyToManyField(Store)   
    product_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    product_class = models.ForeignKey(ProductIdentity, on_delete=models.CASCADE)
    # def __str__(self):
    #     return str(self.name) + str(self.product_id)
    

    

    def save(self, *args, **kwargs):
        if(self.qrcode_text == None):
                qrcode_img = qrcode.make(self.name)
                self.qrcode_text = qrcode_img
                self.slug_field = slugify(self.name) + str(random.randint(9,99))
                # img_field = self.image   
                # image = Image.open(img_field)
                # w,h = image.size      
                # output_size = (300,350)
        super().save(*args, **kwargs) 

    
    def update(self, *args, **kwargs):   
        file_name = ''
       #if(val == image):
        make_thumbnail(self)

        file_name = get_file_name(self.image.name,'_front_image',self.slug_field)        

        slug_str = "%s %s" % (self.name, self.image.name) 
        slug_str = slugify(slug_str) + str(random.randint(9, 9999))
        self.image.name = slug_str + ".jpg" if len(slug_str) < 99 else str(slug_str[0:95])+'.jpg'
        self.image.save(file_name, self.image, save = False)

        
        file_name = get_file_name(self.image_rear.name,'_rear_image',self.slug_field)

        slug_str = "%s %s" % (self.name, self.image_rear.name) 
        slug_str = slugify(slug_str) + str(random.randint(9, 99))
        self.image_rear.name = slug_str + ".jpg" if len(slug_str) < 99 else str(slug_str[0:95])+"_rear_image.jpg"
        self.image_rear.save(file_name, self.image_rear, save = False)

        file_name = get_file_name(self.image_side1.name,'_side1_image',self.slug_field)
        slug_str = "%s %s" % (self.name, self.image_side1.name) 
        slug_str = slugify(slug_str) + str(random.randint(9, 99))
        self.image_side1.name = slug_str + ".jpg" if len(slug_str) < 99 else str(slug_str[0:95])+"_side1_image.jpg"
        self.image_side1.save(self.image_side1.name, self.image_side1, save = False)
        store = self.store.all().first()
        if(self.product_id is None):
            product_id = str(store.store_id) + str(random.randint(100000,999999))
            self.product_id = product_id
        super().save(*args, **kwargs) 
        return self.product_id         
       
    class Meta:
        abstract = True


def get_file_name(name, suffix, slug_field):
        image_name, image_extension = os.path.splitext(name)
        image_name = image_name.replace('-','')
        image_extension = image_extension.lower()
        slug_str = "%s" % (image_name) 
        slug_str = slugify(slug_str) + str(random.randint(9, 99)) + image_extension
        image_filename = image_name + suffix + "product_%s" %slug_field + image_extension
        return image_filename


class ProductDetails(models.Model):
    #specific_name = models.CharField(max_length=100)
    weight=models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    height=models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    width=models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    depth=models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    primary_color = models.CharField(max_length=30)
    other_colors = models.CharField(max_length=150, blank=True, null=True)
    material = models.CharField(max_length=100)
    is_discounted = models.BooleanField(default=False, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
   # product = models.OneToOneField(Product, on_delete=models.CASCADE)
    #is_available = models.BooleanField(default=True)
    quantity = models.IntegerField()   
    quantity_unit = models.CharField(max_length=20,choices=quantity_unit,default='Pieces')
    colors_available = models.CharField(max_length=200, blank=True, null=True)
    origin_country = models.CharField(max_length=50, blank=True, default='INDIA')
    manufacturer_name = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        abstract = True       
      

class Article(Product):
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class ArticleDetails(ProductDetails):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    # def save(self, *args, **kwargs):
    #     print(self)
    #     super.save(*args, **kwargs)
        
    def __str__(self):
        return self.article.name


class GarmentSubcategory (models.Model):
    name = models.CharField(max_length=50)

    class Meta:
           verbose_name_plural = 'GarmentSubcategories'

    def __str__(self):
        return str(self.name)


StandardGarmentSizes = [
          ('S','Small'),
          ('M','Medium'),
          ('L','Large'),
          ('XL','XL'),
          ('XXL','XXL'),
          ('XXXL','XXXL'),
]

class GarmentClassification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


# class Garment(Product):    
#     GARMENT_CATEGORY = (
#         ('Men', "Men's Wear"),
#         ('Women',"Women's Wear"),
#         ('Infant', "Baby wear"),
#         ('Boy', "Boys wear"),
#         ('Girl',"Girls Wear"),
#         # ('Ethnic', "Ethnic Wear"),
#         # ('Designer','Designer Wear'),
#         # ('Casual', 'Casual'),
#         # ('Party', 'Party Wear'),
#         # ('Uniform', 'School Uniform')
#     )
#     #name = models.CharField(max_length=100)
#     #product = models.OneToOneField(Product,on_delete=models.CASCADE)
#     #fabric = models.CharField(max_length=30)
#     #category = MultiSelectField(choices = GARMENT_CATEGORY)
#     #_classification = models.ForeignKey(GarmentClassification, on_delete=models.CASCADE)    
    
#     def save(self, *args, **kwargs):
#             if(self.product_id == None):
#                 self.product_id = '6109' + str(random.randint(9, 99))
#             super().save(*args, **kwargs) 

    
#     def __str__(self):
#         return str(self.name) + ' id:'+ str(self.product_id)


class GarmentDetails(ProductDetails):
    
    season = (
        ('Rainy', 'Rainy'),
        ('Spring', 'Spring'),
        ('Winter', 'Winter'),
        ('Autumn', 'Autumn'),
        ('Summer', 'Summer'),
        ('Standard','Standard')
    )

    neck_design = (
        ('Round', 'Round'),
        ('V-neck' , 'V-neck'),
        ('PoloCollar','PoloCollar'),
        ('NA','Not Applicable')
    )
    
    design_patterns = (
          ('Checks','Checks'),
          ('Floral','Floral'),
          ('Stripes','Stripes'),
          ('Plain','Plain'),
          ('Prints','Prints'),
          ('Dots','Dots'),
          ('Logos','Logos'),
          ('Slogans','Slogans'),
          ('Others','Others')
      )
    # used_for = (
    #     ('upperbody','upperbody')
    #     ('lowerbody','lowerbody')
    #     ('head','head')
    #     ('feet','feet')
    #     ('hands' , 'hands' 
    # )
    garment = models.OneToOneField(Article, on_delete=models.CASCADE)
    pockets_qty = models.IntegerField(default=1, blank=True)
    #zip_qty = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    #subcategory = models.ManyToManyField(GarmentSubcategory)
    #suitable_season = MultiSelectField(choices = season)
    neck_design = models.CharField(max_length=20, choices=neck_design, default='Round')
    design_pattern = MultiSelectField(choices = design_patterns)
    sizes_available = MultiSelectField(choices=StandardGarmentSizes)
    class Meta(ProductDetails.Meta):
           verbose_name_plural = 'GarmentDetails'

    def __str__(self):
        return str(self.garment.name)


class Inventory(models.Model):
    clothing = models.ManyToManyField(Article)
    # jewellery = models.ManyToManyField()


# class KitchenItem(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)


class KitchenItemDetails(ProductDetails):
    kitchen_item = models.OneToOneField(Article, models.CASCADE)

    def __str__(self):
        return str(self.kitchen_item.name)

# class StationeryItem(Product):
    # def __str__(self):
    #     return self.name + ' id:' + str(self.product_id)

class StationeryItemDetails(ProductDetails):
    stationery_item = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.stationery_item.name)

# class SportsFitnessEquipment(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)

class SportsFitnessEquipmentDetails(ProductDetails):
    sports_fitness_equipment = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.sports_fitness_equipment.name)

# class HomeDecor(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)

class HomeDecorDetails(ProductDetails):
    HomeDecor = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.HomeDecor.name)

# class HomeAppliance(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)

class HomeApplianceDetails(ProductDetails):
    home_appliance = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.home_appliance.name)

# class ProductType(models.Model):
#     name = models.CharField(max_length=100, unique=True)


# class Cart(models.Model):
#     products = models.ManyToManyField(Inventory)



