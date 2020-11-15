from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from stores.models import States, StoreCategory, StoreSubcategory
from accounts.models import Seller
from django.utils import timezone
from django import forms
#from .forms import SellerForm

#from api.models import Product


# Create your views here.

def Home(request):
    return render(request,'frontend/Home.html')    

def Login(request):
    return render(request,'frontend/Login.html')

def SignUp(request):
    # if request.method == "POST": 
    #     print('I am enjoying Django')
    #     #form = SellerForm(request.POST)
    #     #print(form)
    #    # if form.is_valid():
    #     print('yes')
    #     first_name = request.POST['first_name']
    #     last_name = request.POST['last_name']
    #     email = request.POST['email']
    #     contact_no_primary = request.POST['mobile_no']
    #     state = request.POST['state']
    #     city = request.POST['city']
    #     password = request.POST['password']
    #     last_login= timezone.now

    #     inst = Seller.objects.create_seller(first_name=first_name,
    #     last_name=last_name,
    #     email=email,
    #     contact_no_primary=contact_no_primary,
    #     state=state,
    #     city=city,
    #     login_password=password,
    #     last_login=last_login)      

    #     inst.save()

        
        
        # return render(request,'frontend/SignUp.html')
   
    # else:
        # states = States.STATE_UT 
        # store_categories = StoreCategory.objects.all()
        # store_subcategories = StoreSubcategory.objects.all()
        # #dynamic_content = DynamicPageContent.breif_signup_hindi  
        context = {'states' : "states", 'store_categories' : "store_categories", 'store_subcategories' : "store_subcategories"}
        # print('no')
        return render(request,'frontend/SignUp.html', context)


def Products(request,type):
    query = request.GET.get('type')
    message="{}".format(query)
    template="frontend/Products.html"
    context={
        'message': message
    }
    return render(request,template,context)


def FetchProducts(request,type):
    
   # products = Product.objects.all()
    #productsM = Product.objects.filter()
    #context = {'states' : states}
    #serializer=ArticleSerializer(articles, many=True)
    return render(request,'frontend/Products.html')


def index(request):
    if request.method == "POST":
        print(request.POST)


