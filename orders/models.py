from django.db   import models

from core.models import Core

class Order(Core):
    order_number = models.IntegerField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders'
