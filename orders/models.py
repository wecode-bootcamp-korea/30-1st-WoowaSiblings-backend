from django.db   import models

from core.models import TimeStamp

class OrderStatusCode(models.Model):
    order_status_code = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order_status_codes'

class Order(TimeStamp):
    order_number      = models.CharField(max_length=400)
    order_status_code = models.ForeignKey('OrderStatusCode', on_delete=models.CASCADE)
    user              = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders'
        
class OrderItemStatusCode(models.Model):
    order_item_status_code = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_item_status_codes'

class OrderItem(TimeStamp):
    quantity               = models.PositiveIntegerField()
    product_time           = models.ForeignKey('products.Time', on_delete=models.CASCADE)
    order                  = models.ForeignKey('Order', on_delete=models.CASCADE)
    order_item_status_code = models.ForeignKey('OrderItemStatusCode', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'order_items'
