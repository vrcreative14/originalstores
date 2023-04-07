from django.db import models
from accounts.models import User
import random
import os

# Create your models here.

def get_upload_path(self, title):
        #seller_id = request.session['seller']
        # if seller_id:
        #         seller_name = Seller.objects.filter(seller = seller_id)
        #         seller_name = seller_name + seller_id
        #         return os.path.join("static/images/products/seller_%d/category_%d" %seller_name ,self.product_class,name)
        # else: 
                file_path = os.path.join("static/images/posts/author_%s" %str(random.randint(9, 99))+str(self.author.id)+str(random.randint(9, 99)),title)
                path_folders = file_path.split("\\")
                if os.path.exists(file_path):
                    file_path = path_folders[0] + "/" + path_folders[1] + "/" + title
                
                    #file_path = os.path.join("static/images/products/store_%s" %self.store.all().first().store_id,"product_%s" %self.slug_field,name)
                return file_path


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    place = models.CharField(max_length=50, blank= True)
    content_initial = models.TextField()
    content_middle = models.TextField()
    content_conclusion = models.TextField()
    image1 = models.ImageField(upload_to = get_upload_path, blank=True)
    image2 = models.ImageField(upload_to = get_upload_path, blank=True)
    image3 = models.ImageField(upload_to = get_upload_path, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

