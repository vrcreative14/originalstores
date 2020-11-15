from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="Name"),
    path('login', views.Login,name="Login"),
    path('SignUp', views.SignUp,name="SignUp"),
    path('Home',views.Home,name="Home"),    
    path('Products/<type>/', views.FetchProducts),
    path('Sign', views.index, name="Submit")
]