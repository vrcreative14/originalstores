from django.contrib import admin
from django.urls import path, re_path
from rest_framework import routers
from .views import UserViewSet
from django.conf.urls import include
from . import views
from knox import views as knox_views


router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('seller/register/', views.RegisterSeller, name='register-seller'),
    path('store/create/', views.RegisterStore, name='create-store'),
    path('store/add/', views.storeCreate, name='add-store'),
    path('auth/seller-list', views.GetSellers.as_view(), name='seller-list'),
    path('auth/user', views.GetUser.as_view(), name='get-user'),
    #path('auth/store-list', views.GetSellers, name='seller-list'),
    #path('store-list/<str:pk>/', views.GetSellerbyId, name='sellerbyId'),
    path('store-list/<str:pk>/', views.GetSellerbyUserId, name='sellerbyId'),
    re_path("^login/$", views.LoginAPI.as_view()),
    #re_path("^login/phone/$", views.LoginAPI.as_view()),
    re_path("^logout/$", knox_views.LogoutView.as_view(), name='knox_logout'),
    re_path("^validate_mobile_otp/$", views.ValidatePhoneOTP.as_view()),
    path("api/auth", include('knox.urls')),
    
   # path("api/auth/register",RegisterAPI.as_views()),
]
