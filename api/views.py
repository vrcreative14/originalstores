from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from accounts.models import User, UserOTP, PhoneOTP
from .serializers import *
from accounts.models import Seller
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .renderers import UserRenderer
#from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from stores.models import Store, StoreCategory, StoreSubcategory
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from django.core.mail import send_mail
from django.conf import settings
from .utils import otp_generator
import sys
import random
# Create your views here.

#link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from='
#link1 = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from=ORIGST&templatename=MobileVerificationOTP&var1={first_name}&var2={user_otp}'

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
            otp = send_otp(phone, usr_first_name)
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
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
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
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
            })





class ValidatePhoneOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password'
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
                'detail' : 'Either phone or otp was not recieved in Post request'
            })


@api_view(['POST'])
def RegisterSeller(request):
    sellerid = request.data.get("seller")
    print(sellerid)
    try:
        usr = request.data.get('user')
        usr_first_name = request.data.get('first_name')
        print(usr)
        phone_no = usr['phone']
    except:
        phone_no = None

    if phone_no:
        phone = str(phone_no)
        validate_phone_otp(phone, usr_first_name)

    serializer = SellerUserSerializer(data=request.data)
    # user = UserSerializer()
    #try:
    if serializer.is_valid(raise_exception=ValueError):
            seller = serializer.save()
            usr_otp = random.randint(100000, 999999)
            print(seller.user)
            UserOTP.objects.create(user = seller.user, otp = usr_otp)
            msg = f"Hello {seller.first_name} \n Your OTP is {usr_otp} \n Thanks"

            send_mail(
                "Welcome to the world of Vykyoo - Verify Your Email",
                msg,
                settings.EMAIL_HOST_USER,
                [seller.user.email],
                fail_silently=False
            )

            # print('seller serializer data:',json.dump(serializer.data,4) )
            #serializer.create(validated_data=request.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)              
    
    # except:
    #     e = sys.exc_info()[0]
    #     print(e)
    return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)




class Register(APIView):
    
    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        email = request.data.get('email', False)
        first_name = request.data.get('first_name', False)
        last_name = request.data.get('last_name', False)
        if phone and password:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False,
                 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'phone': phone, 'password': password }

                        serializer = SellerUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status' : True, 
                            'detail' : 'Congrts, user has been created successfully.'
                        })

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
                'detail' : 'Either phone or password was not recieved in Post request'
            })


# class RegisterSeller(generics.GenericAPIView):
#       serializer_class = SellerSerializer

#       def post(self, request, *args, **kwargs):
#                 serializer = self.get_serializer(data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 user = serializer.save()
#                 return Response({
#                 "user": UserSerializer(user, context=self.get_serializer_context()).data,
#                 "token": AuthToken.objects.create(user)
#                 })


@login_required()
@api_view(['POST'])
def RegisterStore(request):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    user_id = request.data["seller"]
    seller = Seller.objects.get(user = user_id)    
    categories = StoreCategory.objects.filter(name = request.data["store_category"])
    sub_categories = StoreSubcategory.objects.filter(name = request.data["store_subcategory"])
    
    print(user_id)
    print(categories)
    print(sub_categories)
    print(request.data)
    print(seller)
    print('*******') 
    print(seller.id)
    print('*******') 
    store = Store.objects.create(
        seller_id = seller.id,
        name = request.data["name"],
        state = request.data["state"],
        city = request.data["city"],
        pincode = request.data["pincode"]     
    )

    for category in categories:
        store.store_category.add(category)

    for sub_category in sub_categories:
        store.store_subcategory.add(sub_category)
    print('*******')    
    print(store)
    print('*******')    

    print(store.__dict__)
    print(store.store_category)
    serializer = StoreSerializer(data = store.__dict__)
    if serializer.is_valid(raise_exception=ValueError):
        
        serializer.save()
        print(serializer.data)
        #serializer.create(validated_data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

# @login_required()
# @api_view(['GET'])
# def GetSellers(request):
#     permission_classes = (permissions.IsAuthenticated, )  
#     #user_id = request.data["id"]
#     seller = Seller.objects.all()   
#     serializer=SellerSerializer(seller, many=True)
#     return Response(serializer.data)



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


# class RegisterSeller(APIView):
#     """
#     A class based view for creating and fetching student records
#     """
#     # def get(self, format=None):
#     #     """
#     #     Get all the student records
#     #     :param format: Format of the student records to return to
#     #     :return: Returns a list of student records
#     #     """
#     #     students = UnivStudent.objects.all()
#     #     serializer = StudentSerializer(students, many=True)
#     #     return Response(serializer.data)

#     def post(self, request):
#         """
#         Create a student record
#         :param format: Format of the student records to return to
#         :param request: Request object for creating student
#         :return: Returns a student record
#         """
#         serializer = SellerSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=ValueError):
#             serializer.create(validated_data=request.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.error_messages,
#                         status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        print('result for request data is:')
        print(request.data)        
        try:
            print(request.data["phone"])  
            phone = request.data["phone"]                  
            serializer = MobileNoLoginSerializer(data = request.data)       
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
            login(request, user[0], backend='accounts.backends.PhoneBackend')
            return super().post(request, format=None)     
        except:
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
def storeCreate(request): 
    permission_classes = (permissions.IsAuthenticated,)  
    serializer = StorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


def send_otp(phone, usr_first_name):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:        
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        seller_name = str(usr_first_name)
        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
        link =  f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from=ORIGST&templatename=MobileVerificationOTP&var1={seller_name}&var2={otp_key}'
        #result = requests.get(link, verify=False)

        return otp_key
    else:
        return False
