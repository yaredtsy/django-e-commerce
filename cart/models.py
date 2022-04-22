from django.db import models
from store.models import Product,Variation
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    qunatity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.qunatity
    def __unicode__(self):
        return self.product