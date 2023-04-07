from django.db import models

# Create your models here.

class Content(models.Model):
    page_name = models.CharField(max_length=100)
    sub_heading = models.CharField(max_length=500)
    language = models.CharField(max_length=100)
    heading = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    instructions = models.CharField(max_length=500)
    
    def __str__(self):
        return self.sub_heading

class PageContent(models.Model):
    key = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=100)
    value = models.CharField(max_length=10000)
    
    def __str__(self):
        return self.key

    
