from django.db.models import fields
from rest_framework import serializers
from accounts.models import ContactForm, User
from rest_framework.authtoken.models import Token
from accounts.models import Seller
from django.contrib.auth import authenticate
from stores.models import Store,StoreDetails, StoreCategory, StoreSubcategory
from django.contrib.auth import login
from products.models import  *
import random
from orders.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','name','phone','email','password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)        
        return user


class SellerUserSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model= Seller
        fields=('pk','user','first_name', 'last_name')  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = UserSerializer.create(user_serializer, validated_data=user_data)
        seller = Seller.objects.create(user=user,
                            first_name=validated_data.pop('first_name'), last_name=validated_data.pop('last_name'))

        return seller


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Seller
        


class StoreCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = StoreCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductCategory


class StoreSubCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = StoreSubcategory


class StoreSerializer(serializers.ModelSerializer):
    store_category = StoreCategorySerializer(read_only = True, many=True)
    product_category = ProductCategorySerializer(read_only=True, many=True)   
    
    
    class Meta:
        model = Store
        fields=('seller','name','state','city','pincode','latitude','longitude','store_category','product_category','storeimage')


    def create(self, validated_data, *args, **kwargs):
        
        store = Store.objects.create(**validated_data)            
        return store

        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email','password', 'phone']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()   
    pft = serializers.CharField(
        style={'input_type':'password'}, trim_whitespace = False
    )

    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email')      
        pft = attrs.get('pft')

        if email and pft:
            if User.objects.filter(email = email).exists():                
                
                user = User.objects.get(email = email)
                if user.check_password(pft):
                    user = User.objects.get(email = email)
                else:
                    msg = {'detail' : 'Password Incorrect'}
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = {'detail' : 'Email is not registered', 'register' : False }
                raise serializers.ValidationError(msg, code='authorization')
        
        else:
            msg = 'Must include email and password.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class MobileNoLoginSerializer(serializers.Serializer):
    
    
    phone = serializers.CharField()
    pft = serializers.CharField(
        style={'input_type':'password'}, trim_whitespace = False
    )

    def validate(self, attrs):
        print(attrs)        
        
        phone = attrs.get('phone')
        password = attrs.get('pft')

        if phone and password:
            if User.objects.filter(phone = phone).exists():
                               
                
                user = User.objects.get(phone = phone)
                if user.check_password(password):
                    user = User.objects.get(phone = phone)
                else:
                    msg = {'detail' : 'Password Incorrect'}
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = {'detail' : 'Mobile number is not registered', 'register' : False }
                raise serializers.ValidationError(msg, code='authorization')
        
        else:
            msg = 'Must include "Mobile number" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class StorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDetails
        fields = '__all__'

class Prod_Details_Serializer(serializers.ModelSerializer):
    
    def create(self, validated_data, *args, **kwargs):
        article_details = ArticleDetails.objects.create(**validated_data)
        print(article_details)
        return article_details

    class Meta:
        model = ArticleDetails
        fields = ('article','primary_color','material','description','quantity')


class Product_Serializer(serializers.ModelSerializer):    
    
    class Meta:
        model = Article
        fields = ('name','price','brand_name','image','image_rear','image_side1')
        
   

class Garment_Serializer(serializers.ModelSerializer):    
    store = StoreSerializer(read_only=True,many = True)
    class Meta:
        model = Article
        fields = ['name','image','img_path','brand_name','price','category','store']

class GarmentDetailsSerializer(serializers.ModelSerializer):    
    store = StoreSerializer(read_only=True,many = True)
    class Meta:
        model = GarmentDetails
        fields = ['garment','pockets_qty','description','neck_design','design_pattern','sizes_available']


class ShippingAddressSerializer(serializers.ModelSerializer):
    
    
    def create(self, validated_data, *args, **kwargs):
             
        shipping_address = ShippingAddress.objects.create(**validated_data)            
        return shipping_address

    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['ref_code', 'user', 'payment_status', 'items', 'destination']

class SubmitContactSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return super().create(validated_data)
    class Meta:
        model = ContactForm
        fields = ['full_name','phone','email','message']
