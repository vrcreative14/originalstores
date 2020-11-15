from rest_framework import serializers
from accounts.models import User
from rest_framework.authtoken.models import Token
from accounts.models import Seller
from django.contrib.auth import authenticate
from stores.models import Store, StoreCategory, StoreSubcategory
from django.contrib.auth import login


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','email','password', 'phone']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #token = Token.objects.create(user=user)
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


class StoreSubCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = StoreSubcategory


class StoreSerializer(serializers.ModelSerializer):
    store_category = StoreCategorySerializer(read_only = True, many=True)
    store_subcategory = StoreSubCategorySerializer(read_only = True, many=True)
    seller = SellerSerializer(read_only = True, many=True)
    print(serializers.ModelSerializer)
    class Meta:
        model = Store
        fields=('seller_id','seller','name','state','city','pincode','store_category','store_subcategory')

    # def create(self, validated_data):
    #     #email = validated_data.pop('seller')
    #     #user = User.objects.get(email = email)            
    #     print('*******')
    #     print(validated_data.pop('seller'))
    #     store = Store.objects.create(seller = validated_data.get('seller'),
    #                             name=validated_data.pop('name'),
    #                             state=validated_data.pop('state'),
    #                             city=validated_data.pop('city'),
    #                             pincode=validated_data.pop('pincode')                                
    #                             )
    #     print(store)                                
    #     return store
       


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email','password', 'phone']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    # def validate(self, attrs):
    #     email = attrs.get('email', '')
    #     username = attrs.get('username', '')

    #     if not username.isalnum():
    #         raise serializers.ValidationError(
    #             self.default_error_messages)
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #Token.objects.create(user=user)
        return user
# class StudentSerializer(serializers.ModelSerializer):
#     """
#     A student serializer to return the student details
#     """
#     user = UserSerializer(required=True)

#     class Meta:
#         model = UnivStudent
#         fields = ('user', 'subject_major',)

#     def create(self, validated_data):
#         """
#         Overriding the default create method of the Model serializer.
#         :param validated_data: data containing all the details of student
#         :return: returns a successfully created student record
#         """
#         user_data = validated_data.pop('user')
#         user = UserSerializer.create(UserSerializer(), validated_data=user_data)
#         student, created = UnivStudent.objects.update_or_create(user=user,
#                             subject_major=validated_data.pop('subject_major'))
#         return student


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()   
    password = serializers.CharField(
        style={'input_type':'password'}, trim_whitespace = False
    )

    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email')      
        password = attrs.get('password')

        if email and password:
            if User.objects.filter(email = email).exists():
                print(email, password)
                #user = authenticate (request = self.context.get('request'),email = email, password = password)
                user = User.objects.filter(email = email)
            else:
                msg = {'detail' : 'Email is not registered', 'register' : False }
                raise serializers.ValidationError(msg, code='authorization')
        
        else:
            msg = 'Must include email and password.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class MobileNoLoginSerializer(serializers.Serializer):
    
    #email = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'}, trim_whitespace = False
    )

    def validate(self, attrs):
        print(attrs)
        
        #email = attrs.get('email')
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if User.objects.filter(phone = phone).exists():
                print(phone, password)
                #user = authenticate(request = self.context.get('request'),phone = phone, password = password,backend='accounts.backends.PhoneBackend')
                #login(self.context.get('request'),user, backend='django.contrib.auth.backends.ModelBackend')
                user = User.objects.filter(phone = phone)
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




# # Login Serializer
# class LoginSerializer(serializers.Serializer):
#   username = serializers.CharField()
#   password = serializers.CharField()

#   def validate(self, data):
#     user = authenticate(**data)
#     if user and user.is_active:
#       return user
#     raise serializers.ValidationError("Incorrect Credentials")

