from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.contrib import auth
import re
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,name, email,phone, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email and not phone:
            raise ValueError("Users must have either an email address or mobile number")
        if not password:
            raise ValueError("Users must have a password")

        
        user_obj = self.model(
            name=name,
            email = self.normalize_email(email),
            phone = phone,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff  #change user password
        user_obj.admin = is_admin  #change user password
        user_obj.active = is_active  #change user password
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self,name, email,phone, password=None):
        user = self.create_user(
            name,
            email,
            phone,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self,name, email,phone, password=None):
        if not phone:
            phone = None
            user = self.create_user(
                name,
                email,
                phone,
                password=password,
                is_staff=True,
                is_admin=True
            )
        else:    
            user = self.create_user(
                name,
                email,
                phone,
                password=password,
                is_staff=True,
                is_admin=True
            )
            return user
    
    
user_types = [
    ('seller','Seller'),
    ('carrier','Carrier'),
    ('seller','Seller'),
    ('seller','Seller'),
]

class User (AbstractBaseUser):    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    name = models.CharField(max_length=150)
    #first_name = models.CharField(max_length=20)
    #last_name = models.CharField(max_length=20)
    #name = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_carrier = models.BooleanField(default=False)
    #designation = models.CharField(max_length=20, choices=neck_design, default='Round')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # def __init__(self, institute, *args, **kwargs):
    #     super().__init__()
    #     #self.helper = FormHelper()
    #     self.fields['designation'].queryset = User.objects.filter(institute_id=user)
    #     self.fields['department'].queryset = Department.objects.filter(institute_id=institute)
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def save(self, *args, **kwargs):
             # Empty strings are not unique, but we can save multiple NULLs
            if not self.email:
                self.email = None

            super().save(*args, **kwargs)  # Python3-style super()

    # def save(self, *args, **kwargs):
    #         regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #         # ... other things not important here
    #         #self.email = self.email.lower().strip()  # Hopefully reduces junk to ""
    #         if self.email != "":                     # If it's not blank
    #             if not (re.search(regex,self.email)):    # If it's not an email address
    #                 raise ValidationError(u'%s is not an email address, dummy!' % self.email)
    #         if self.email == "":
    #             self.email = None
    #         super(User, self).save(*args, **kwargs)

    # def clean(self):
    #             #     """
    #             # Clean up blank fields to null
    #             # """
    #         if self.email == "" :
    #             self.email = None


class Seller(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    seller_email = models.EmailField(max_length=255, blank=True, null=True)
    seller_phone = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    secondary_email = models.EmailField(max_length=255, blank=True, null=True)
    secondary_phone = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)    
    joining_date = models.DateField(auto_now_add=True)
    is_business_registered = models.BooleanField(default=False)
    business_name = models.CharField(max_length=50, blank=True)
    is_physical_store = models.BooleanField(default=True)
    
    def __str__(self):
        return self.first_name
    



class SellerDetails(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=255, blank=True)
    contact_no_primary = models.CharField(max_length=13, blank=True, unique=True)
    contact_no_secondary = models.CharField(max_length=13, blank=True)    
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    primary_pincode = models.CharField(max_length=6, blank=True)    


    def __str__(self) :
        return self.seller



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # email = models.CharField(max_length=50)
    # contact_no_primary = models.CharField(max_length=13, blank=True)
    # contact_no_secondary = models.CharField(max_length=13, blank=True)    
    joining_date = models.DateField(auto_now_add=True)
    # last_login = models.DateTimeField()
    
    def __str__(self):
         return self.first_name

class CustomerDetails(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=255, blank=True)
    contact_no_primary = models.CharField(max_length=13, blank=True, unique=True)
    contact_no_secondary = models.CharField(max_length=13, blank=True)    
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    primary_pincode = models.CharField(max_length=6, blank=True)
    #last_login = models.DateTimeField()


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=9)
    count = models.IntegerField(default=0)


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    otp = models.CharField(max_length = 9, blank = True, null = True)
    count = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged  = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot  = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')
    
    def __str__(self):
            return 'OTP code:' + str(self.otp) + "sent to" + str(self.phone)


class ContactForm(models.Model):    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    message = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.email
