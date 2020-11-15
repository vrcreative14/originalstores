from django.db import models
from accounts.models import Seller

# Create your models here.

class CompanyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) :
        return self.name


class Organization(models.Model):    
    name = models.CharField(max_length=50)
    is_registered = models.BooleanField()
    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_DEFAULT, default=1)
    is_gst_registered = models.BooleanField()
    gstin = models.CharField(max_length=15 , blank=True)

    def __str__(self) :
        return self.name
    

class Popularity(models.Model):
    likes = models.IntegerField(default=0)
    favourite = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural='Popularity'


class StoreCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural='StoreCategories'
    
    def __str__(self) :
        return self.name

class StoreSubcategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
           verbose_name_plural = 'StoreSubcategories'

    def __str__(self) :
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) :
        return self.name


class States(models.Model):
    STATE_UT = (
        ( 'Andaman and Nicobar Islands'),
        ('Andhra Pradesh'),
        ( 'Arunachal Pradesh'),
        ( 'Assam'),
        ( 'Bihar'),
        ( 'Chandigarh'),
        ( 'Chhattisgarh'),
        ( 'Dadra and Nagar Haveli'),
        ( 'Daman and Diu'),
        ( 'Delhi'),
        ( 'Goa'),
        ('Gujarat'),
        ( 'Haryana'),
        ( 'Himachal Pradesh'),
        ( 'Jammu and Kashmir'),
        ( 'Jharkhand'),
        ( 'Karnataka'),
        ( 'Kerala'),
        ( 'Lakshadweep'),
        ( 'Madhya Pradesh'),
        ( 'Maharashtra'),
        ( 'Manipur'),
        ( 'Meghalaya'),
        ( 'Mizoram'),
        ( 'Nagaland'),
        ( 'Orissa'),
        ( 'Pondicherry'),
        ( 'Punjab'),
        ( 'Rajasthan'),
        ( 'Sikkim'),
        ( 'Tamil Nadu'),
        ( 'Tripura'),
        ( 'Uttarakhand'),
        ( 'Uttar Pradesh'),
        ( 'West Bengal'),         
    )


class StoreManager(models.Model):
    name=models.CharField(max_length=50)
    designation=models.ForeignKey(Designation, on_delete=models.SET_DEFAULT, default='Manager')
    mobileno=models.CharField(max_length=13)
    emailid=models.EmailField(max_length=254)
    joining_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.name)



class Store(models.Model):
    
    STATE_UT = (
        ('AN', 'Andaman and Nicobar Islands'),
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CG', 'Chhattisgarh'),
        ('DH', 'Dadra and Nagar Haveli'),
        ('CG', 'Daman and Diu'),
        ('DL', 'Delhi'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('LD', 'Lakshadweep'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Orissa'),
        ('PY', 'Pondicherry'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TR', 'Tripura'),
        ('UK', 'Uttarakhand'),
        ('UP', 'Uttar Pradesh'),
        ('WB', 'West Bengal'),         
    )
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)    
    state = models.CharField(max_length=25, choices=STATE_UT)
    city = models.CharField(max_length=30)
    pincode = models.CharField(max_length=6)
    latitude = models.CharField(max_length=20, default='26.8467° N')
    longitude = models.CharField(max_length=20, default='80.9462° E')
    #owner_name = models.CharField(max_length=50)
    #email_id = models.EmailField(max_length=254)
    store_manager = models.ForeignKey(StoreManager, on_delete=models.SET_DEFAULT,default=1, blank=True)
    store_category = models.ManyToManyField(StoreCategory)
    store_subcategory = models.ManyToManyField(StoreSubcategory)
    #store_category = models.ForeignKey(StoreCategory, on_delete=models.SET_DEFAULT, default=1)
    img_path = models.CharField(max_length=50,blank=True)
    storeimage = models.ImageField(upload_to='images/store', height_field=None, blank=True)
    #store_details = models.ForeignKey(StoreDetails, on_delete=models.CASCADE, blank=True)                    # relation with details and hence further with organization
    def __str__(self):
        return str(self.name)


class StoreDetails(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    specifications = models.CharField(max_length=50, blank=True)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    nearest_landmark = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    people_accomodation_capacity = models.IntegerField(default=10)
    no_of_helpers = models.IntegerField(default=4)
    safety_status = models.BooleanField(default=True)
    is_parking_available = models.BooleanField(default=False)
    is_already_online = models.BooleanField(default=False)
    popularity = models.ForeignKey(Popularity, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1, blank=True)
    
    class Meta:
        verbose_name_plural='StoreDetails'

    def __str__(self):
        return str(self.specifications)