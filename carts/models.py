from django.db   import models

from core.models import Core

class Cart(Core):
    quantity       = models.IntegerField()
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_option = models.ForeignKey('products.Product_option', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'carts'
    
