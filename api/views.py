from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from rest_framework import viewsets, permissions
from rest_framework import response
from rest_framework.decorators import api_view
from accounts.models import User, UserOTP, PhoneOTP
from .serializers import *
from accounts.models import Seller
from accounts.models import UserOTP
from rest_framework.response import Response
from django.http import  JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .renderers import UserRenderer
#from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from knox.views import LoginView as KnoxLoginView, LogoutView
from knox.auth import TokenAuthentication
from django.contrib.auth import login, logout
from stores.models import Store, StoreCategory, StoreSubcategory,States,StoreDetails
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from django.core.mail import send_mail
from .utils import otp_generator
import sys
import random
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import parser_classes
from products.models import *
from orders.models import *
import json
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
import pytz
utc = pytz.UTC
# Create your views here.

#link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from='


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



def validate_phone_otp(phone, usr_first_name):        
        user = User.objects.filter(phone = phone)
        if user.exists():
            return Response({
                'status':False,
                'detail':'Mobile number already exists'
            })
        else:
            otp = send_otp(phone,4)
            if otp:
                otp = str(otp)
                count = 0
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first().count()
                    old.first().count = count + 1
                    old.first().save()

                else:
                    count = count + 1       
                    PhoneOTP.objects.create(
                        phone = phone,
                        otp = otp,
                        count = count
                    )

                    if count > 5:
                        return Response({
                            'status':'False',
                            'detail':'Error in sending OTP, Limit exceeded. Please contact customer support.'
                        })
                    
                    # old.count = count + 1
                    # old.save()
                    print("count increase", count)
                    return Response({
                        'status' : True,
                        'detail': 'OTP sent successfully'
                    })
                PhoneOTP.objects.create(
                    phone = phone,
                    otp = key
                )
                pass
            else:
                return Response({
                    'status':False,
                    'detail':'Error in sending OTP'
                })



class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        # user_name = request.data.get('name')
        phone_number = request.data.get('phone')
        # if user_name:
        #     user_name = str(user_name)
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone, 4)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old_otp_obj = old.first()
                        old_otp_obj.otp = otp
                        old_otp_obj.count = count + 1
                        old_otp_obj.save(force_update=True)
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                                phone =  phone, 
                                otp =   otp,
                                count = count        
                                )

                    if count > 5:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'An SMS with an OTP(One Time Password) has been sent <br/> to your Mobile number'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "We haven't received any phone number. Please do a POST request."
            })


class ValidatePhoneOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password    
    '''
    def post(self, request, *args, **kwargs):

        try:
            phone = request.data.get('mobile', False)
            otp_sent = request.data.get('otp', False)           

        except:
            return Response({
                            'status' : False, 
                            'detail' : 'Please provide required fields.'
                        })

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    # temp_data = {'name': name,'phone': phone,'email':email,'password': password }
                    # if(RegisterUser(temp_data)):                        
                    return Response({
                            'status' : True, 
                            'detail' : 'OTP matched'
                        })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not received'
            })


@login_required(login_url='http://127.0.0.1:8000/login')
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def RegisterSeller(request):    
    usr = request.data.get('user', False)
    first_name = request.data.get('firstname', '')
    middle_name = request.data.get('middlename', '')
    last_name = request.data.get('lastname', '')
    seller_email = request.data.get('primaryemail', '')
    seller_phone = request.data.get('primarymobile','')
    secondary_email = request.data.get('secondaryemail', '')
    secondary_phone = request.data.get('secondarymobile', '')
    is_business_registered = request.data.get('is_business_registered', False)
    business_name = request.data.get('business_name','')
    is_store_physical = request.data.get('is_physical_store', False)

    try:
        user_phone = request.session['user_phone']
        user_email = request.session['user_email']
        user = User.objects.get(phone = user_phone) if user_phone != '' else User.objects.get(email = user_email)
        
        Temp_data = {'user': user.pk, 'first_name' : first_name,'middle_name': middle_name,'last_name': last_name, 'secondary_email': secondary_email, 'secondary_phone': secondary_phone,
        'seller_email':seller_email,'seller_phone':seller_phone,'secondary_email':secondary_email,
        'secondary_phone':secondary_phone,'is_business_registered':is_business_registered,
        'business_name':business_name,'is_physical_store':is_store_physical}
      
    except:
       return Response({
           'status': False,
           'detail': 'Please provide User Data'
       })
   

    serializer = SellerSerializer(data=Temp_data)
    # user = UserSerializer()
    try:
        if serializer.is_valid(raise_exception=ValueError):
            serializer.errors
            seller = serializer.save()
            # usr_otp = random.randint(100000, 999999)
            # print(seller.user)
            # UserOTP.objects.create(user = seller.user, otp = usr_otp)
            #msg = f"Hello {seller.first_name} \n Your OTP is {usr_otp} \n Thanks"

            # send_mail(
            #     "Welcome to the world of Vykyoo - Verify Your Email",
            #     msg,
            #     settings.EMAIL_HOST_USER,
            #     [seller.user.email],
            #     fail_silently=False
            # )

            # print('seller serializer data:',json.dump(serializer.data,4) )
            #serializer.create(validated_data=request.data)
            #Seller Information saved successfully.We will contact you at your mobile number:'+seller_phone+' for further verification. Continue filling the Store Info
            
            request.session['seller'] = seller.pk
            resp =  Response({
                'status': True,
                'detail':'Seller Information saved successfully. Continue saving the Store Details',
            }, status.HTTP_201_CREATED)                      
            return resp
            #return Response(serializer.data,status=status.HTTP_201_CREATED)              
    
    except:
         e = sys.exc_info()[0]
         print(e)
         return Response({
             'status':False,
             'detail':e
         })
        #return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)


# @login_required(login_url='http://127.0.0.1:8000/login')

class RegisterStore(APIView):
        permission_classes = [permissions.IsAuthenticated]
        #parser_classes = [MultiPartParser]

        def post(self, request, format = None):
                #user_ph = request.data.get('user_ph', '')
                #user = User.objects.get(phone = user_ph)
                input_gstin = ''
                user_phone = request.session.get('user_phone', None)
                user = ''
                if user_phone is None:
                    user_email = request.session.get('user_email', None)
                    if(user_email is None):
                        Logout(request)
                    user = User.objects.filter(email = user_email)
                else:
                    user = User.objects.filter(phone = user_phone)

                seller = Seller.objects.get(user = user[0].pk)
                is_gst_registered = request.data.get("is_gst_registered", False)
                if is_gst_registered:
                            input_gstin = request.data.get("gstin",False)
                else:
                            input_gstin = None
                store_existing = Store.objects.filter(seller = seller.pk)                 
                if len(store_existing) > 0:
                            check_existing = StoreDetails.objects.filter(gstin = input_gstin)
                            if len(check_existing) > 0:
                                 if(check_existing[0].store.seller.pk != seller.pk):
                                     return Response({
                                          'status' : False,
                                          'detail':'This GSTIN is already regstered with another Seller'
                                     })                                   
                
                name = request.data.get('shopname', False)
                state = request.data.get('state', False)
                city = request.data.get('city', False)
                pincode = request.data.get('pincode', False)
                latitude = request.data.get('latitude', False)
                longitude = request.data.get('longitude', False)
                product_categories = request.data.get('productcategory','')
                store_categories = request.data.get('storecategory','')
                product_categories_list = []
                store_category_list = []
                #    # storeimage = request.data["storeimage"]
                for category in product_categories:
                    prod_category = ProductCategory.objects.filter(name = category)
                    product_categories_list.append(prod_category[0].pk)
                
                for store_category in store_categories:
                    category = StoreCategory.objects.filter(name = store_category)
                    store_category_list.append(category[0].pk)

                temp_data = {"seller": seller.pk, "name": name, "state": state, "city" : city, "pincode": pincode, "latitude": latitude, "longitude": longitude,"store_category":store_categories,"product_category":product_categories }

                serializer = StoreSerializer(data= temp_data)
                if serializer.is_valid():
                        store = serializer.save()
                else:
                        send_mail(
                            'errors',
                            'detail'+ serializer.errors,
                            'vcnityonline@gmail.com',
                            ['vrcreative14@gmail.com'],
                            fail_silently=False,
                        )
                        
               
                address_line1 = request.data.get("address")
                landmark = request.data.get("landmark", "")                                          
                details_data = {"store":store.pk, "address_line1": address_line1, "nearest_landmark": landmark,"is_gst_registered":is_gst_registered ,"gstin": input_gstin}
                serializer2 = StoreDetailsSerializer(data = details_data)
                if serializer2.is_valid():
                            serializer2.save()                           
                            return JsonResponse({
                                'status': True,
                                'detail': 'Store Successfully Created. Continue saving further information',
                                'store' : store.pk
                            })
                else:
                            error = serializer.errors
                            return Response({
                               'status': False,
                               'detail': error
                            })
        
        def create(self, request, *args, **kwargs):
                user_phone = request.session["user_phone"] 
                user = ''
                if user_phone is None:
                            user_email = request.session["user_email"]
                            user = User.objects.filter(email = user_email)
                else:
                            user = User.objects.filter(phone = user_phone)

                seller = Seller.objects.get(user = user[0].pk)
                name = request.data.get('shopname', False)
                state = request.data.get('state', False)
                city = request.data.get('city', False)
                pincode = request.data.get('pincode', False)
                latitude = request.data.get('latitude', False)
                longitude = request.data.get('longitude', False)
                product_categories = request.data.get('productcategory','')
                store_categories = request.data.get('storecategory','')
                store_id  = str(self.pincode) +str(self.pk)+ str(random.randint(9, 99))
                new_store = Store.objects.create(name = name,seller = seller.pk,state=state,city = city,pincode = pincode,latitude=latitude,longitude=longitude,product_category= product_categories,store_category=store_categories,store_id=store_id)
                new_store.save()
                product_categories_list = []
                store_category_list = []
                        #    # storeimage = request.data["storeimage"]
                for category in product_categories:
                            prod_category = ProductCategory.objects.filter(name = category)
                            #product_categories_list.append(prod_category[0].pk)
                            new_store.product_category.add(prod_category[0])
                        
                for store_category in store_categories:
                            category = StoreCategory.objects.filter(name = store_category)
                            new_store.store_category.add(category[0])


        def patch(self, request):
            pk = request.data["store"]
            model = get_object_or_404(Store, pk=pk)
            storeimage = request.data["storeimage"]
            model.storeimage = storeimage
            model.save()
            return Response({
                'status': True,
                'detail': 'Image uploaded succcesfully'
            }) 
        #     temp_data = {"storeimage" : storeimage}
        #     serializer = StoreSerializer(Store,data= temp_data, partial = True)

        #     if serializer.is_valid():
        #         serializer.save(update_fields=['storeimage'])
        #         return Response(serializer.data)
        # # return a meaningful error response
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductDetails(APIView):
        #permission_classes = [permissions.IsAuthenticated]
        #parser_classes = [MultiPartParser]

        def post(self, request, format = None):
                product_id = request.data.get('product_id')
                article = Article.objects.get(product_id = product_id)
                request.data['article'] = article.pk
                # user_ph = request.data.get('user_ph', '')
                # user = User.objects.get(phone = user_ph)
                # seller = Seller.objects.get(user = user.pk)
                # name = request.data.get('shopname', False)
                # state = request.data.get('state', False)
                # city = request.data.get('city', False)
                # pincode = request.data.get('pincode', False)
                # latitude = request.data.get('latitude', False)
                # longitude = request.data.get('longitude', False)
               
               # storeimage = request.data["storeimage"]

               #temp_data = {"seller": seller.pk, "name": name, "state": state, "city" : city, "pincode": pincode, "latitude": latitude, "longitude": longitude}

                serializer = Prod_Details_Serializer(data= request.data)
                if serializer.is_valid():
                   prod = serializer.save()
                   response = Response({
                       'status': True,
                       'detail': 'Product Details have been saved successfully'
                   })
                   response.set_cookie('messageText',str("Product Details have been saved successfully"),24*60*60*1) 
                   response.set_cookie('messageType','true',24*60*60*1)                             
                   return response
                #    if prod:
                #         address_line1 = request.data.get("address")
                #         landmark = request.data.get("landmark", "")
                #         is_gst_registered = request.data.get("is_gst_registered", False)
                #         gstin = request.data.get("gstin")

                #         details_data = {"store":store.pk, "address_line1": address_line1, "nearest_landmark": landmark,"is_gst_registered":is_gst_registered ,"gstin": gstin}
                #         serializer2 = StoreDetailsSerializer(data = details_data)
                #         if serializer2.is_valid():
                #             serializer2.save()                           
                #             return JsonResponse({
                #                 'status': True,
                #                 'detail': 'Store Successfully Created. Continue saving further information',
                #                 'store' : store.pk
                #             })
                # else:
                #     error = serializer.errors
                #     return Response({
                #         'status': False,
                #         'detail': error
                #     })
        
        def patch(self, request):
            pk = request.data["store"]
            model = get_object_or_404(Store, pk=pk)
            storeimage = request.data["storeimage"]
            model.storeimage = storeimage
            model.save()
            return Response({
                'status': True,
                'detail': 'Image uploaded succcesfully'
            })


class AddProduct(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format = None):
        seller_id = request.session['seller']
        if seller_id is None:
            return redirect('/SellerRegistration');
        store = Store.objects.filter(seller = 2)
        name = request.data.get('product_name', '')
        price = request.data.get('product_price', '')
        brand_name = request.data.get('brand_name', '')
        sub_category_name = request.data.get('select_subcategory', '')        
        identity_name = request.data.get('select_identity', '')
        image = request.data.get('image','')
        image_rear = request.data.get('image_rear','')
        image_side1 = request.data.get('image_side1','')
        selected_stores = request.data.get('selected_stores',[])
        store_ids = [j.store_id for j in Store.objects.filter(seller = seller_id)]
        stores_list = []
        for store in store_ids:
            stores_list.append(str(request.data.get('store_id'))) if request.data.get('store_id') else print('no store')


        # if len(selected_stores) > 0:
        #     for stores in selected_stores:
                
        sub_category = ProductSubCategory.objects.filter(name = sub_category_name)
        product_class = ProductIdentity.objects.filter(name = identity_name)
        #image_thumbnail = request.data.get('product_image_front_thumb','')
        temp_data = {'name': name, 'price':price, 'brand_name':brand_name,'image':image,'store':store,'product_category':sub_category[0].pk,'product_class':product_class[0].pk}
        #image_rear = request.data.get('image_rear','')
        #image_side1 = request.data.get('image_side1','')
        
        serializer = Product_Serializer(data = temp_data)
        if serializer.is_valid():
                # if(image.name == image_rear.name):
                # return Response({
                #     'status':False,
                #     'detail':'Rear Image Of Product is exactly same as '
                # })
                try:
                        product_sub_category = ProductSubCategory.objects.get(name = sub_category_name)
                        product_class = ProductIdentity.objects.get(type = product_sub_category.pk,name = identity_name)
                        new_product = Article.objects.create(name = name, brand_name = brand_name,
                        price = price, product_category = product_sub_category, product_class=product_class)
                        #new_product.store.add(Store.objects.get(id))
                        #prod = serializer.create(validated_data = serializer.data)
                        for store_id in stores_list:
                            new_product.store.add(Store.objects.get(store_id = store_id))
                        
                        new_product.image = image
                        new_product.image_rear = image_rear
                        new_product.image_side1 = image_side1
                        result = new_product.update()
                        #image_rear = image_rear,image_side1 = image_side1)
                        return Response({
                            'status': True,
                            'detail': "Product added succesfully",
                            'data': result,
                        },status.HTTP_201_CREATED)
                
                except Exception as e: 
                        if not e.args[0].find("does not have storage.objects.delete access to vicinity-solutions.appspot.com") == -1:
                            return Response({
                                'status':False,
                                'detail':"Image with same name exists already. Try changing the name of images uploaded."
                            })
                        return Response({
                            'status': False,
                            'detail': "Product could not be saved due to some error.Please Try again"
                        },status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({
                'status': False,
                'detail':'Product could not be saved'
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request,  pk):
        product = Article.objects.get(pk = pk)
        if product is None:
            return Response({
                'status':False,
                'detail':'Product does not exists.'
            })
        seller_id = request.session['seller']
        if seller_id is None:
            return redirect('/SellerRegistration');
        store = Store.objects.filter(seller = 2)
        name = request.data.get('product_name', '')
        price = request.data.get('product_price', '')
        brand_name = request.data.get('brand_name', '')
        sub_category_name = request.data.get('select_subcategory', '')        
        identity_name = request.data.get('select_identity', '')
        image = request.data.get('image','')
        image_rear = request.data.get('image_rear','')
        image_side1 = request.data.get('image_side1','')
        selected_stores = request.data.get('selected_stores',[])
        store_ids = [j.store_id for j in Store.objects.filter(seller = seller_id)]
        stores_list = []
        for store in store_ids:
            stores_list.append(str(request.data.get('store_id'))) if request.data.get('store_id') else print('no store')


        # if len(selected_stores) > 0:
        #     for stores in selected_stores:
                

        sub_category = ProductSubCategory.objects.filter(name = sub_category_name)
        product_class = ProductIdentity.objects.filter(name = identity_name)
        #image_thumbnail = request.data.get('product_image_front_thumb','')
        temp_data = {'name': name, 'price':price, 'brand_name':brand_name,'image':image,'store':store,'product_category':sub_category[0].pk,'product_class':product_class[0].pk}
        #image_rear = request.data.get('image_rear','')
        #image_side1 = request.data.get('image_side1','')
                
        serializer = Product_Serializer(product,data = temp_data)
        if serializer.is_valid():
                try:
                        serializer.update()
                        #new_product.store.add(Store.objects.get(id))
                        #prod = serializer.create(validated_data = serializer.data)
                        # for store_id in stores_list:
                        #     new_product.store.add(Store.objects.get(store_id = store_id))
                        return Response({
                            'status': True,
                            'detail': "Product Info saved succesfully"
                        },status.HTTP_201_CREATED)
                
                except Exception as e:
                        if not e.args[0].find("does not have storage.objects.delete access to vicinity-solutions.appspot.com") == -1:
                            return Response({
                                'status':False,
                                'detail':"Image with same name exists already. Try changing the name of images uploaded."
                            })
                        return Response({
                            'status': False,
                            'detail': "Product could not be saved due to some error.Please Try again"
                        },status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({
                'status': False,
                'detail':'Product could not be saved'
            }, status.HTTP_400_BAD_REQUEST)



def RegisterUser(temp_data):
        try:
            serializer = UserSerializer(data=temp_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            u=user.save()
            return True
        
        except:
            return False

# @api_view(["GET"])
# def GetProducts(request):
#     category = request.data.get

class Register(APIView):
    
    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('mobile', False)
        password = request.data.get('pw', False)
        email = request.data.get('email', False)
        name = request.data.get('name', False)
        otp = request.data.get('otp', False)
       
        if phone and password:
            phone = str(phone)
            if email:
                user_email = User.objects.filter(email__iexact = email)
                if user_email.exists():
                    return Response({'status': False,
                    'detail': 'Email entered is already registered.Try with different Email OR <br/> <a href="/login">Login into existing account from here</a>'})

            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False,
                 'detail': 'Phone number entered is already registered.Try with different mobile number OR <br/> <a href="/Login">Login into existing account from here</a>'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'name':name,'phone': phone,'email':email, 'password': password}

                        serializer = UserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()                       
                        old.delete()
                        request.session['user_name'] = name
                        request.session['phone'] = phone
                        request.session['email'] = email                        
                        resp = Response({
                            'status' : True, 
                            'detail' : 'User registered successfully'
                        })
                        #resp.set_cookie('user', user.pk)
                        request.session['user'] = user.pk
                        return resp
                        # return Response({
                        #     'status' : True, 
                        #     'detail' : 'User registered successfully'
                        # })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'
                        })
                else:
                    return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognised. Kindly request a new otp with this number'
                })              


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or password was not received '
            })


class GetSellers(generics.ListAPIView):
        permission_classes = [permissions.IsAuthenticated,] 
        serializer_class=SellerSerializer
        def get_object(self):            
            seller = Seller.objects.all()   
            serializer=SellerSerializer(seller, many=True)
            return Response(serializer.data)


class GetUser(generics.RetrieveAPIView):
        permission_classes = [permissions.IsAuthenticated,] 
        serializer_class = UserSerializer
    
        def get_object(self):  
             return self.request.user


@login_required()
@api_view(['GET'])
def GetSellerbyId(request,pk):
    seller = Seller.objects.get(id = pk)
    serializer = SellerSerializer(seller, many=False)
    return Response(serializer.data)

@login_required()
@api_view(['GET'])
def GetSellerbyUserId(request,pk):
    user = User.objects.get(id = pk)
    seller = Seller.objects.get(user = user.id)
    serializer = SellerSerializer(seller, many=False)
    return Response(serializer.data)


class RegisterView(generics.GenericAPIView):
    
    serializer_class = SellerSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        #Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        print('result for request data is:')
        print(request.data)        
        user_obj = ''
        try:
            print(request.data["phone"])
            user_phone = request.data["phone"]                  
            serializer = MobileNoLoginSerializer(data = request.data)       
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user.is_active == False:
                    return Response({
                    'status': False,
                    'detail':'Please verify your Mobile number through OTP, before logging in.'
                })
            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user, backend='accounts.backends.PhoneBackend')           
            user_obj = user
            # request.session['user_token'] = b.data

            #return response           
       
        except Exception as e:            
            if(not str(e.args[0]).find("Mobile number is not registered") == -1):
                    return Response({
                           'status' : False,
                           'detail' : 'Entered Mobile number is not registered. <a style="font-size:15px;font-weight:300;" href="/SignUp"> New users Signup from here</a>',                          
                            })
            
            elif(not str(e.args[0]).find("Password Incorrect") == -1):
                    return Response({
                           'status' : False,
                           'detail' : 'Password Incorrect',},status.HTTP_401_UNAUTHORIZED)

            serializer = LoginSerializer(data = request.data)                            
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user.is_active == False:
                return Response({
                    'status': False,
                    'detail':'Please verify your Email through OTP, before logging in.'
                })

            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')            
            user_obj = user
            # v = super().post(request, format=None)
            # HttpResponse.set_cookie("atl",v.data["token"],expires=v.data["expiry"],httponly=True)
            # return v
        request.session['userid'] = user_obj.pk
        request.session['user_name'] = user_obj.name.split(" ")[0]
        request.session['user_phone'] = user_obj.phone 
        request.session['user_email'] = user_obj.email 
        seller = Seller.objects.filter(user = user_obj.pk)
        if len(seller) > 0:
            request.session['seller'] = seller[0].pk
        else:
            request.session['seller'] = None
        response = super().post(request, format=None)
        auth_token = response.data["token"]
        # expiry = response.data["expiry"]
        response.set_cookie('tkl',auth_token,24*60*60*10,httponly=True) 
        return response       
                #response.set_cookie('upl', user_phone, 24*60*60*10)                
       
                #response.set_cookie('uel', user_email, 24*60*60*10)          
        # return Response({
        #     'status':True,
        #     'Detail':'Logged in Successfully'
        # })


class LogoutAPI(LogoutView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        print(request)
        v = logout(request)
        response =  Response({'status': True,'detail': 'You have been logged out Successfully.'})
        response.delete_cookie('upe')
        response.delete_cookie('tkl')
        response.set_cookie('messageText','You have been Logged out successfully',24*60*60*1) 
        response.set_cookie('messageType','true',24*60*60*1)            
        redirect_to = request.GET.get('redirectTo',None)
        if redirect_to is not None:
            return redirect(redirect_to)
        return response        
    

def Logout(request):
        v = logout(request)
        response =  Response({'status': True,'detail': 'You have been logged out Successfully.'})
        response.delete_cookie('upe')
        response.delete_cookie('tkl')
        response.set_cookie('messageText','You have been Logged out successfully',24*60*60*1) 
        response.set_cookie('messageType','true',24*60*60*1)   
        return response         
        #redirect_to = request.GET.get('redirectTo',None)


@api_view(['GET'])
def GetToken(request):    
        #credential = request.data["phone"]    
        credential=request.GET.get('phone', '')
        #user = User.objects.get(phone = credential)
        #if credential == ''
        if credential == '':
            user = User.objects.get(email = credential)
            if user == '':
                user = User.objects.get
                res = Response({'status': False,
                'detail': 'It seems you have been registered. Please Signup and continue.'})
            else:
               res = GetTokenforUser(request,user)

        else:
           res = GetTokenforUser(request,user)
        # def post(self, request, *args, **kwargs):
        #     token = request.COOKIES['atl']
        #     pass
        return res

@api_view(['GET'])
def GetTokenforUser(request):
    tkl = request.COOKIES["tkl"]
    resp = Response({'status':True, 'tkl':tkl})                   
    return resp


@api_view(['POST'])
def AddStoreDetails(request): 
    permission_classes = (permissions.IsAuthenticated,)
    serializer = StoreDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


def send_otp(phone, no_of_digits):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:
        key = otp_generator(no_of_digits)
        phone = str(phone)
        otp_key = str(key)
        user_name = 'Dear Vcnity User'
        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
        #link =  f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from=ORIGST&templatename=MobileVerificationOTP&var1={seller_name}&var2={otp_key}'
        link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from=VCNITY&templatename=Mobile+Number+Verification+OTP&var1={user_name}&var2={otp_key}'
        result = requests.get(link, verify=False)

        return otp_key
    else:
        return False


def LoginHelper(request,password,phone=None, email=None):
     try:            
            login_data = {'phone': phone, 'pft': password}        
            serializer = MobileNoLoginSerializer(data = login_data)       
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user[0].is_active == False:
                    return Response({
                    'status': False,
                    'detail':'Please verify your Mobile number through OTP, before logging in.'
                })
            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user[0], backend='accounts.backends.PhoneBackend')
            b = super().post(request, format=None)  
            request.session['user_token'] = b.data
            return b
            # return Response({
            #     'status' : True,
            #     'detail' : 'Logged in Successfully',
            #     'info' : b,
            # })  

       
     except Exception as e:
            
            if(not str(e.args[0]).find("Mobile number is not registered") == -1):
                    return Response({
                           'status' : False,
                           'detail' : 'Entered Mobile number is not registered. <a style="font-size:15px;font-weight:300;" href="/SignUp"> New users Signup from here</a>',                          
                            })

            serializer = LoginSerializer(data = request.data)                           
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user[0].is_active == False:
                return Response({
                    'status': False,
                    'detail':'Please verify your Email through OTP, before logging in.'
                })

            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user[0], backend = 'django.contrib.auth.backends.ModelBackend')
            return super().post(request, format=None)

@api_view(['POST'])
@parser_classes((MultiPartParser,))
def handle_uploaded_image(request):
    #process image
    if not 'uploaded_media' in request.FILES:
        return Response({'msg':'Photo missing.'},status.HTTP_400_BAD_REQUEST)
    try:
        img = Image.open(StringIO(request.FILES['uploaded_media'].read()))
    except IOError:
        return Response({'msg':'Bad image.'}, status.HTTP_400_BAD_REQUEST)

    serializer = Product_Serializer(data = request.DATA)
    if not serializer.is_valid():
        return Response({'msg':serializer.errors}, status.HTTP_400_BAD_REQUEST)

    clothing = Article.create()


@api_view(['GET'])
def GetProducts(request):
    products = Article.objects.all()
    Temp_data = []
    for product in products:
        print(product)     
        dictionary = {'name':product.name, 'price' : product.price, 'category' : 'Men', 'store' : product.store}
        Temp_data.append(dictionary)
        #Temp_data.append(dictionary)
        # Temp_data.update({'name' : product.name})
        # Temp_data.update({'price' : product.price})
        # Temp_data.update({'category' : 'Men'})
        # Temp_data.update({'store' : product.store})          
  
    serializer = Garment_Serializer(data = Temp_data)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response({'status': False, 'error': serializer.errors}) 


class GarmentViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = Garment_Serializer

class GarmentDetailsViewSet(viewsets.ModelViewSet):
    queryset = GarmentDetails.objects.all()
    serializer_class = GarmentDetailsSerializer


class SaveShipppingAddress(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # is_self_pickup = request.data.get('self_pickup',False)
        # temp_data = {}
        # if is_self_pickup:
        #         order = OrderSerializer(data = )


        # else:                
                user = request.session['userid']
                address_line1 = request.data.get('address_line1', False)
                address_line2 = request.data.get('address_line2', False)
                pincode = request.data.get('pincode', False)
                city = request.data.get('city', False)
                state = request.data.get('state', False)
                addressee_name = request.data.get('addressee_name',False)                
                temp_data = {'user':user,'address_line1':address_line1,'address_line2':address_line2,'addressee_name':addressee_name,'city':city,'state':state,'pincode':pincode }

                serializer = ShippingAddressSerializer(data = temp_data)
                if serializer.is_valid():
                        serializer.save()
                        return Response({
                            'status':True,
                            'detail':'Shipping Address Saved Successfully'
                        }, status.HTTP_201_CREATED)
                
                else:
                        return Response({
                            'status':False,
                            'detail':serializer.errors
                        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_otp_mail(request):
    email = request.data.get('email',None)
    if email is None:
        return Response({
            'status':False,
            'detail':'Please provide valid Email-Id'
        })
    usr = User.objects.filter(email= email)
    #user = request.session['user']
    #seller = request.session['seller']
    #usr = User.objects.filter(pk = user)
    #seller = Seller.objects.filter(pk = seller)
    otp = random.randint(100000, 999999)
    subject = 'OTP for account recovery from vcnity.online'
    detail =  '' 
    count = 0
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    if len(usr) > 0:
        detail ='Your OTP for account password change is ' + str(otp)+'. Enter this OTP at vcnity.online to change your password.'
        old = UserOTP.objects.filter(user = usr[0])
        if old.exists():
           # old = old.first()
            count = old.first().count
            if old.first().count > 7:
                    
                    diff = utc.localize(now) - old.first().time_stamp
                    if diff.days < 24:
                        return Response({
                            'detail':'Maximum number of attempts exhausted.Please try changing password after 24 hours. Contact customer care for more help',
                            'status': False
                        })
                    else:
                        updateOTP(old, otp)
            else:   
                    updateOTP(old, otp)
                    #old.first().count = count + 1
                    #old.first().otp = otp
                    # old.first().save(force_update=True)
                    #result = send_email_registered(subject,detail,email)
        else:
            count = count + 1
            UserOTP.objects.create(
                user = usr[0],
                otp = otp
            )
        result = send_email_registered(subject,detail,email)
        if result:
                request.session['forgot_password_user'] = usr[0].pk
                return Response({
                    'status': True,
                    'detail':'Email with OTP has been sent to the registered email id',
                })
        # registered_email = usr[0].email
        # seller_email = seller[0].seller_email
        # secondary_mail = seller[0].secondary_email
    else:
    #         seller = Seller.objects.filter(seller_email=email)
    #         if len(seller)>0:
    #             seller = Seller.objects.filter(seller_email=email)

    #         else:
    #             seller = Seller.objects.filter(secondary_email=email)
    
    # #if email==registered_email or email==seller_email or email==secondary_mail:
    #         otp = random.randint(100000, 999999)
    #         send_email_registered(subject,detail,email)
            return Response({
                        'status':False,
                        'detail':'The entered Email id is not registered with the User account'
                    })

def updateOTP(old, otp):
    count = old.first().count
    old_otp_obj = old.first()
    old_otp_obj.otp = otp
    old_otp_obj.count = count + 1
    old_otp_obj.save(force_update=True)

@api_view(['POST'])
def send_otp_mobile(request):
    phone = request.data.get('mobile', None)
    if phone is None:
        return Response({
            'detail':"Invalid Mobile number",
            'status':False
        })
    user = User.objects.filter(phone = phone)
    # if len(user) == 0:
    #     
    count = 0
    if user.exists():
            old = UserOTP.objects.filter(user = user[0])
            user = user[0]                                    
            if old.exists():
                    count = old.first().count
                    if count > 5:
                            return Response({
                                'status':'False',
                                'detail':'Error in sending OTP, Limit exceeded. Please contact customer support.'
                            })
                    
                    if otp:
                            otp = str(otp)   
                            request.session['forgot_password_user'] = user.pk                         
                            old_otp_obj = old.first()
                            old_otp_obj.otp = otp
                            old_otp_obj.count = count + 1
                            old_otp_obj.save(force_update=True)

                    else:
                            return Response({
                            'status':False,
                            'detail':'Error in sending OTP'
                        })
                   

            else:
                    otp = send_otp(phone, 6)
                    if otp:
                            request.session['forgot_password_user'] = user.pk      
                            count = count + 1       
                            UserOTP.objects.create(
                                user = user,
                                otp = otp,
                                count = count
                            )
                    else:
                            return Response({
                            'status':False,
                            'detail':'Error in sending OTP'
                        })                    
                    
                    # old.count = count + 1
                    # old.save()
                    print("count increase", count)
                    return Response({
                        'status' : True,
                        'detail': 'OTP matched.Now you can create new password'
                    })
                # PhoneOTP.objects.create(
                #     phone = phone,
                #     otp = key
                # )
                # pass
            return Response({
                    'status':True,
                    'detail':'Email with OTP has been sent to the registered mobile number'
                })            
                            
    else:
            return Response({              
                  'detail':'This Mobile number is not registered.New users can signup from here <a href="/SignUp">Signup</a>',
                  'status': False            
            })           
    pass


@api_view(['POST'])
def check_otp(request):
    credential = request.data.get('cred',None)
    if credential is None:
        return Response({
            'status':False,
            'detail':'Please provide valid Email id/Mobile number'
        })
    val = credential.split('@')
    if len(val) > 1:
        user = User.objects.filter(email= credential)
    else:
        user = User.objects.filter(phone= credential)    
    
    user_otp = UserOTP.objects.filter(user = user[0])
    otp = user_otp[0].otp
    entered_otp = request.data.get('otp',False)
    if entered_otp:
        if otp == entered_otp:
            return Response({
                'status':True,
                'detail':'OTP matched.Now you can create new password'
            })
        else:
            return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
    else:
        return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })

@api_view(['POST'])
def ChangePassword(request):
    changed_password = request.data.get('changedpw',None)
    if changed_password is not None:
        if 'forgot_password_user' in request.session:
            user = request.session['forgot_password_user']
        else:
            return Response({
                'status':False,
                'detail':'Invalid response',
            })
        usr = User.objects.get(pk = user)
        usr.set_password(changed_password)
        usr.save()
        update_session_auth_hash(request, usr)
        del request.session['forgot_password_user']
        response = Response({
                       'status': True,
                       'detail': 'Password changed successfully.Login to your account'
                   })
        response.set_cookie('messageText',str('Password changed successfully.Login to your account'),24*60*60*1) 
        response.set_cookie('messageType','true',24*60*60*1)      
        #redirect_to = request.GET.get('redirectTo',None)
        #if redirect_to is not None:
        
        #    return 
        #return response                       
        return response
    else:
        return Response({
            'status':False,
            'detail':'Invalid Request'
        })

def send_email_registered(subject,detail,email):
    send_mail(
            subject,
            detail,
            'vcnityonline@gmail.com',
            [email],
            fail_silently=False,
            )
    return True


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    pass

@api_view(['POST'])
def SubmitContact(request):
    name = request.data.get('name', '')
    phone = request.data.get('mobile', '')
    email = request.data.get('email', '')
    serializer = SubmitContactSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status':True,
            'detail':'Your details have been saved.<br/> Our team will will contact you shortly.'
        })
    else:
        
        return Response({
            'status':False,
            'detail':'The request for this email or mobile number has already been submitted.'
        }, status.HTTP_400_BAD_REQUEST)
    pass