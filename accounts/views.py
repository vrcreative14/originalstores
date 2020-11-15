from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth

# Create your views here.


# class CustomAuthenticationBackend:
    
#     def authenticate(self, request, email_or_phone=None, password=None):
#         try:
#              user = User.objects.get(
#                  Q(email=email_or_phone) | Q(phone=email_or_phone)
#              )
#              pwd_valid = user.check_password(password)
#              if pwd_valid:            
#                  return user
#              return None
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

    

# def login_page(request):
#     form = LoginForm(request.POST)
#     context = {
#         "form": form
#     }
#     next_=request.GET.get('next')