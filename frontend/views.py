from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Seller
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
import datetime
from stores.models import States, StoreCategory, Store
from products.models import *
from api.utils import convert_toWords
from django.shortcuts import redirect
from orders.models import Order, ShippingAddress
import hashlib
import hmac
import base64
from blogpost.models import BlogPost
#from .forms import SellerForm
#from api.models import Product
# Create your views here.
appId = '59627866e07fd8257a056c53972695'
orderId = 'order00001'
orderAmount = '10'
orderCurrency = 'INR'
orderNote = 'test'
customerName = 'Kartik'
secretKey = 'aecfa278fed6dae860fd93ca39fee75fac1213e0'
customerPhone = '7565897280'
customerEmail = 'mkartik231@gmail.com'
returnUrl = 'http://127.0.0.1:8000/buy/'
notifyUrl = 'http://127.0.0.1:8000/'
def Home(request):
    try:
        #name = request.session['user_name']
        #phone = request.session['phone']
        #token = request.session['user_token']
        user_name = token["user"]["name"]
        date_string = token["expiry"]
        format = "%Y-%m-d"
        #d=datetime.datetime.strftime(float(date_string), format)
        
        context = {'loggedin' : True}

    except Exception as e:
        context = {'loggedin' : False}
    
    # print(request.session)
    # A = ["pim","pom"]
    # B = ["999999999", "777888999"]
    # P = "88999"
    # S = "1222 --   956565"
    
    return render(request,'frontend/Home.html', context)

def solution(S):
    # write your code in Python 3.6
    result = ""
    count = 0
    j = S
    for i in range(len(S)):
        if S[i] == " ":
           j =  S.replace(S[i],"")
        
    for i in range(0,len(S) - 1,3):
        count = count + 1
        check = S[i:i+3]
        if i == 0:
            result = result + check
        
        else:
            if count % 2 == 0:
                result = result + check
            else:
                result = result + "-" + check

    print(result)
# def solution(A, B, P):
#         # write your code in Python 3.6
#         count = len(P)
#         result = []
#         for i in range(len(B)-1):
#             for j in range(0,9,count):
#                     if j+count >= len(B[i])-1:
#                         continue
#                     check = B[i][j:j+count]
#                     if check == P:
#                         result.append(A[i])

#         if len(result) > 1 :
#             result.sort()
#         elif len(result) == 0:
#             return "NO CONTACT"
#         return result[0]  

# def myProgram():
#     list = [7,6,1,3,5]
#     store = []
    # for i in range(len(a)-1):
    #     diff = 0        
    #     diff = a[i] - a[i+1]
    #     if diff > 0:
    #         temp = a[i]

    #     if diff > 1 :
    #         store.append(diff)
    #     elif diff < -1:
    #         store.append(-diff)    
    
    

    # print(list)
    # list = [1,10,100,1000,10000,100000,1000000]
    # for i in list:
    #     dup = i
    #     count = 0
    #     while dup>1:
    #         dup = dup/10
    #         count+=1
    #     if count%2 == 0:
    #             print(i)
    #x = int(input('Please inout an integer'))
    # #print(x)
    # rows = 5
    # max_col = 5
    # for i in range(rows):
    #     count = i*2 + 1
    #     for x in range(count):
    #             print('*', end=' ')
    #     print(' ')
    # pass
    # x = [4,7,8,46,5]
    # for i in range(len(x)):
    #     check = i+1
    # while check < len(x):
    #     if x[i] > x[check]:
    #         x[i] = x[check]
    #     check += 1


def Login(request):
    #put logic here to check whether len(request.GET)==0 OR check that token in cookie has expired..
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'frontend/Login.html')


def SignUp(request):           
        # return render(request,'frontend/SignUp.html')    
        # #dynamic_content = DynamicPageContent.breif_signup_hindi  
        if request.user.is_authenticated:
            return redirect('/')
            
        context = {'states' : "states", 'store_categories' : "store_categories", 'store_subcategories' : "store_subcategories"}
        # print('no')
        return render(request,'frontend/SignUp.html', context)

@login_required(login_url='/login')
def Checkout(request):      
        sign = get_signature()
        user_id = request.session['userid']
        saved_addresses = ShippingAddress.objects.filter(user = user_id)
        context = {'addresses': saved_addresses,'states': States.STATE_UT, 'signature':sign}
        save_address = ''
        # if orders:
        #         saved_address = orders.destination
        return render(request,'frontend/Checkout.html', context)

@login_required(login_url='/login')
def categories(request):
      context = {'states' : "states", 'store_categories' : "store_categories", 'store_subcategories' : "store_subcategories"}
        # print('no')
      return render(request,'frontend/Cart.html', context)


@permission_classes([IsAuthenticated])
@login_required(login_url='/login')
def RegisterSeller(request):
    #token = request.data.get('token', False)    
    # if request.user.is_seller:
    #     return redirect('/SellerDashboard');
    #     # return render(request, 'frontend/SellerDashboard.html')
    # else:
        seller = request.session["seller"]
        if seller is not None:                
                return redirect('/SellerDashboard')

        try:
            token = request.session['user_token']
            user_email = token["user"]["email"]
            user_name = token["user"]["name"]
            categories = ProductCategory.objects.all()
            store_category = StoreCategory.objects.all()
            context = {'loggedin':True,'email' : user_email, 'states': States.STATE_UT, 'categories': categories, 'store_categories': store_category}
        except:            
            categories = ProductCategory.objects.all()   
            store_category = StoreCategory.objects.all() 
            context = {'loggedin':True, 'email' : '', 'states': States.STATE_UT, 'categories': categories, 'store_categories': store_category}

        return render(request,'frontend/SellerRegistration.html',context)

@login_required(login_url='/login')
def SellerDashboard(request):
    stores = Store.objects.filter(seller = request.session.get('seller', None))
    seller = Seller.objects.filter(user = request.user.pk)
    
    if seller is None or len(seller) == 0:
        request.session["seller"] = None
        return redirect('/SellerRegistration')
    #products = ''
    products = []
    if len(stores) > 0:
        for store in stores:
            product = Article.objects.filter(store = store.pk)
            for item in product:                       
                #if len(item) > 0:
                    products.append(item)

    context = {'stores': stores,'seller_name':seller[0].first_name+ ' ' +seller[0].last_name,'products':products}    
    return render(request,'frontend/SellerDashboard.html', context)

@login_required(login_url='/login')
def AddStore(request):
    seller_id = request.session['seller']
    seller = Seller.objects.filter(pk = seller_id)
    categories = ProductCategory.objects.all()
    store_category = StoreCategory.objects.all()
    context = {'states': States.STATE_UT, 'categories': categories, 'store_categories': store_category, 'seller':seller[0]}
    return render(request, 'AddStore.html', context)


def Products(request,type):
    message="{}".format(selected_category)
    template="frontend/Products.html"
    context={
        'message': message
    }
    return render(request,template,context)


def FetchProducts(request):
    
   # products = Product.objects.all()
    #productsM = Product.objects.filter()
    #context = {'states' : states}
    #serializer=ArticleSerializer(articles, many=True)
    fetched_products = []
    dic = {}
    product_category = request.GET.get('category')
    switcher = {
                'clothing':'Fashion & Clothing',
                'household_essentials':'Household Essentials',
                'kitchen_essentials':'Kitchen Essentials',
                'handicrafts_home_decor':'Handicrafts & Home Decor',                          
        }
    selected_category = switcher.get(product_category, None)

    if(selected_category is not None):
        category = ProductCategory.objects.get(name = selected_category)
        sub_categories = ProductSubCategory.objects.filter(type = category.pk)
        keys =range(len(sub_categories))
        for i in keys :
            try:
                prods = Garment.objects.filter(product_category = sub_categories[i].pk)
                for p in prods :                   
                    fetched_products.append(Garment(name = p.name, brand_name=p.brand_name, image = p.image
                    ,price = p.price))   
                if len(prods) != 0:
                    dic[sub_categories[i].name] = fetched_products    
            #print(sub_category)
            except Exception as e:
                print("An exception occurred: ", e) 
                continue
        
        pass
    print(dic)
    category = request.GET.get('category','')
    categories = ProductCategory.objects.all()
    article = Garment.objects.all()
    context = {'articles' : article,}
    return render(request,'frontend/Products.html', context)

def ViewBlogs(request):
    blogs = BlogPost.objects.all()
    context = {'blogs': blogs}
    return render(request,'frontend/Blogs.html', context)
 
def BlogsDetailed(request):
    id = request.GET.get('dveucvuyr3vybrvbcurbno')
    blog = BlogPost.objects.get(pk = id)
    #next_blog = blog.get_next_by_created()
    context = {'blog' : blog}

    return render(request, 'frontend/BlogDetails.html', context)


def index(request):
    if request.method == "POST":
        print(request.POST)


@login_required(login_url='/login')
def AddProducts(request):
    categories = ProductCategory.objects.all()    
    seller_id = request.session['seller']
   
    product_slug = request.GET.get('product','')
    product = Article.objects.filter(slug_field = product_slug)
    if seller_id :
            store = Store.objects.filter(seller = seller_id)
    if len(product) > 0:
        prod = product[0]
        #category = ProductSubCategory
        context = {'name':prod.name, 'product_category':prod.product_category.type.name, 'product_subcategory':prod.product_category.name,'product_identity':prod.product_class.name,
        'image_front':prod.image.url,'image_rear':prod.image_rear.url,'image_side1':prod.image_side1.url,'price':prod.price,'brand_name':prod.brand_name,
        'productcategories': categories, 'stores':store,'product_id':prod.pk }
    else:    
        context = {'productcategories': categories, 'stores':store, 'material':'Fabric'}
    return render(request,'frontend/AddProducts.html', context)


@login_required(login_url='/login')
def AddBlogPost(request):
    categories = ProductCategory.objects.all()    
    seller_id = request.session['seller']      
    
    return render(request,'frontend/AddBlogPost.html')


def SelectedProduct(request):
    category = request.GET.get('category','')
    default_items = []
    context = {}
    sub_categories = []
    articles = []
    sub_category_obj = []
    # if category == 'clothing':
    default_items = ['T-Shirts','Formal Shirts','Casual Shirts','Formal Trousers','Lowers','Jeans & Casual Tousers']
    default_items_menu_class = 'ui bottom attached inverted ' + convert_toWords(len(default_items)) + ' item menu'
    #selected_product_categories = ProductSubCategory.objects.filter(type = 1012)
    selected_product_category = ProductCategory.objects.filter(name = category)
    if len(selected_product_category) > 0:
        sub_category = get_default_subcategory(category)
        sub_category_obj = ProductSubCategory.objects.filter(type = selected_product_category[0].pk, name = sub_category)
    
    if len(sub_category_obj) > 0:                   
            articles = Article.objects.filter(product_category = sub_category_obj[0].pk, is_approved=True).order_by('-id')

    
    item_in_words = convert_toWords(len(sub_categories))
    div_class_name = 'ui ' +  item_in_words + ' item secondary pointing menu'    
    
    context = {'category':category,'selected_product_categories' : sub_categories,'articles':articles ,'div_class_name': div_class_name,'default_items':default_items,'default_items_menu_class':default_items_menu_class}        
    return render(request,'SelectedProductList.html',context)


def ProductDetails(request):
    slug = request.GET.get('details','')
    context = {}
    if slug:
        article = Article.objects.get(slug_field = slug)
        article_details = ArticleDetails.objects.get(article = article.pk)
        context = {'article': article,'details':article_details}
    return render(request,'frontend/ProductDetails.html', context)


def get_default_subcategory(category):

        switcher={
            'Fashion & Clothing':"Men's Wear",
            'Home Appliances':'Refrigerators',
            'Kitchen Essentials':'Kitchen Appliances',
            'Electronic Devices':'Television',
            'Groceries':'Thursday',
            'Personal Care':'Friday',
            'Automobile Accesories':'Saturday'
        }
        return switcher.get(category,"Invalid")

def get_signature():

        postData = {
        "appId" : appId,
        "orderId" : orderId,
        "orderAmount" : orderAmount,
        "orderCurrency" : orderCurrency,
        "orderNote" : orderNote,
        "customerName" : customerName,
        "customerPhone" : customerPhone,
        "customerEmail" : customerEmail,
        "returnUrl" : returnUrl,
        "notifyUrl" : notifyUrl
        }

        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+postData[key];

        message = bytes(signatureData, encoding = 'utf8')
        #get secret key from your config
        secret = bytes(secretKey, encoding = 'utf8')
        signature = base64.b64encode(hmac.new(secret, message,digestmod=hashlib.sha256).digest())
        return signature

def Volunteer(request):
    type = request.GET.get('type','')   
    context = {'type' : type}
    return render(request, 'frontend/Volunteer.html', context)

def contact_us(request):    
    return render(request, 'frontend/ContactUs.html')

def online_store(request):    
    return render(request, 'frontend/SellerDashboard.html')
#signature = get_signature()
def cart(request):
    return render(request, 'frontend/Checkout.html')

