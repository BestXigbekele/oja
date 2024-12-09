from django.db import models
from django.contrib.auth.models import User



    
class SubCategory(models.Model):
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category

class products(models.Model):
    category2 = models.ManyToManyField(SubCategory, related_name='products')
    name=models.CharField( null=False,max_length=100)
    Amount=models.PositiveIntegerField(null=False)
    price = models.DecimalField(null=False,max_digits=10, decimal_places=2)
    image=models.ImageField(null=False,upload_to='iamges2')
    date_time=models.DateTimeField()
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()