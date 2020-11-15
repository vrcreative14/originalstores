from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.contrib import auth
#from django.contrib.auth.models import User
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email,phone, password=None, is_staff=False, is_admin=False, is_active=False):
        if not email and not phone:
            raise ValueError("Users must have either an email address or mobile number")
        if not password:
            raise ValueError("Users must have a password")

        
        user_obj = self.model(
            email = self.normalize_email(email),
            phone = phone,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff  #change user password
        user_obj.admin = is_admin  #change user password
        user_obj.active = is_active  #change user password
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self, email,phone, password=None):
        user = self.create_user(
            email,
            phone,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email,phone, password=None):
        user = self.create_user(
            email,
            phone,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user
    


class User (AbstractBaseUser):    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    #first_name = models.CharField(max_length=20)
    #last_name = models.CharField(max_length=20)
    #name = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    
    def __str__(self):
        return self.email


    def get_full_name(self):
        return self.email

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



class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    #email = models.EmailField()    
   # login_password = models.CharField(max_length=50)
   # organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=5)
    joining_date = models.DateField(auto_now_add=True)
    
    def __str__(self) :
        return self.first_name
    
    # def __str__(self):
    #     return "{0} {1}".format(self.user.first_name,self.user.last_name)
    # extend extra data



class SellerDetails(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=255, blank=True)
    contact_no_primary = models.CharField(max_length=13, blank=True, unique=True)
    contact_no_secondary = models.CharField(max_length=13, blank=True)    
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    primary_pincode = models.CharField(max_length=6, blank=True)
    #last_login = models.DateTimeField()


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
    otp = models.IntegerField()


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    otp = models.CharField(max_length = 9, blank = True, null = True)
    count = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    
    def __str__(self):
            return 'OTP code:' + str(self.otp) + "sent to" + str(self.phone)