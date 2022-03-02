from django.db   import models

from core.models import Time_stamp

class Order_status_code:
    order_status_code = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order_status_code'

class Order(Time_stamp):
    order_number      = models.CharField(max_length=400)
    order_status_code = models.ForeignKey('Order_status_code', on_delete=models.CASCADE)
    user              = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders'
        
class Order_item_status_code:
    order_item_status_code = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_item_status_code'

class Order_item(Time_stamp):
    quantity               = models.PositiveIntegerField()
    product_time           = models.ForeignKey('products.Time', on_delete=models.CASCADE)
    order                  = models.ForeignKey('Order', on_delete=models.CASCADE)
    order_item_status_code = models.ForeignKey('Order_item_status_code', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'order_items'
