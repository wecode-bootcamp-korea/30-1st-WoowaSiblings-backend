from xmlrpc.client import Boolean, boolean
from django.db   import models

from core.models import Core

class Thirtyth(Core):
    name            = models.CharField(max_length=100)
    status_message  = models.CharField(max_length=300)
    big_image_url   = models.CharField(max_length=300)
    small_image_url = models.CharField(max_length=300)
    is_posible      = models.BooleanField(default=True)
    category        = models.ForeignKey('products.Category', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'thirtyth'
