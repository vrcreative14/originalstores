from django.db import models
from accounts.models import User
from products.models import Article
from stores.models import STATE_UT
# Create your models here.

Payment_Status = [
    ('Paid','Paid'),
    ('EMI' , 'EMI'),
    ('COD', 'Cash on Delivery')
]

Order_Status = [
    ('Cancelled','Cancelled'),
    ('Confirmed','Confirmed'),
    ('Delivered','Delivered'),
    ('On Way','On its way')
]

Cart_Item_Status = [
    ('Added','Added'),
    ('Removed','Removed'),
    ('Ordered','Ordered'),
]

class CartItem(models.Model):
    item = models.OneToOneField(Article, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30,choices=Cart_Item_Status,default='Added')

    def __str__(self):
        return self.item.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    
    def get_cart_items(self):
            return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return self.user.name


class OrderedItem(models.Model):
    item = models.OneToOneField(Article, on_delete=models.PROTECT)
    order_status = models.CharField(max_length=30,choices=Order_Status,default='Confirmed')
    timestamp = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addressee_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=30, choices=STATE_UT)
    city = models.CharField(max_length=30)
    pincode = models.CharField(max_length=6)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, null=True, blank=True)

    # def save(self,*args, **kwargs):
    #     if self.user.name is not None:
    #         self.addressee_name = self.user.name
        
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name

    

class Order(models.Model):
    ref_code = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    date_ordered = models.DateTimeField(auto_now_add=True)    
    payment_status = models.CharField(max_length=30,choices=Payment_Status,default='COD')
    items = models.ManyToManyField(OrderedItem)
    destination = models.OneToOneField(ShippingAddress, on_delete=models.PROTECT, blank=True)
    def __str__(self):
        return self.destination.user.name


class SavedCardsForPay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name_on_card = models.CharField(max_length=100, blank=True)
    card_number = models.CharField(max_length=20)
    date_valid = models.DateField()
    cvv_code = models.CharField(max_length=6)


    
     
    