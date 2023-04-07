from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="Name"),
    path('login', views.Login,name="Login"),
    path('SignUp', views.SignUp,name="SignUp"),
    path('Home',views.Home,name="Home"),       
    path('Sign', views.index, name="Submit"),
    path('vikreta', views.RegisterSeller, name="SellerRegistration"),
    path('SellerDashboard', views.SellerDashboard, name="SellerDashboard"),
    path('AddProducts', views.AddProducts, name="AddProducts"),   
    path('Checkout', views.Checkout, name="AddProducts"),
    path('Products/', views.SelectedProduct),    
    path('AddStore/', views.AddStore, name="AddStore"),    
    path('products/details/', views.ProductDetails, name="ProductDetails"),    
    path('buy/', views.Checkout, name="CheckOut"),    
    path('register/', views.Volunteer, name="register"),    
    path('blogs/', views.ViewBlogs, name="blogs"),    
    path('blogs/detail/', views.BlogsDetailed, name="blogs"),    
    path('blogs/add/', views.AddBlogPost, name="addblogs"),    
    path('contact-us', views.contact_us, name="contact-us"),    
    path('online-store', views.online_store, name="online-store"),
    path('cart', views.cart, name="cart"),
]