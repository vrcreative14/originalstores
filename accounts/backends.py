from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

customuser = get_user_model()

class PhoneBackend(BaseBackend):
    def authenticate(self,request,username,password=None, **kwargs):
       
        try:
           # Try to fetch the user by searching the username or email field
            #user = customuser.objects.get(User(email=username)|User(phone=username))
            user = User.objects.get(phone = username)
            # if user.check_password(password):
            #     return user
        # except user.MultipleObjectsReturned: 
        #     user = User.objects.filter(phone = username).order_by('id').first()

        except customuser.DoesNotExist:
            return None
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            #customuser().set_password(password)

        if getattr(user, 'is_active') and user.check_password(password):
            return user
        print(user.check_password(password))
        print(getattr(user, 'is_active'))

    def get_user(self, user_id):
        
        try:
          return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None