from django.db   import models

from core.models import TimeStamp

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'categories'
    
class Product(TimeStamp):
    name           = models.CharField(max_length=200)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    stock          = models.PositiveIntegerField()
    on_discount    = models.BooleanField()
    product_option = models.BooleanField()
    category       = models.ForeignKey('Category', on_delete=models.CASCADE)
    service_detail = models.ForeignKey('ServiceDetail', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products' 
        
class ProductTime(TimeStamp):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    time    = models.ForeignKey('Time', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_time'

class Time(TimeStamp):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'times'
    
class ThumbnailImage(TimeStamp):
    thumbnail_image_url  = models.CharField(max_length=400)
    product              = models.OneToOneField('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'thumbnail_images'

class ServiceDetail(TimeStamp):
    content = models.CharField(max_length=400)
    
    class Meta:
        db_table = 'service_details'  
        
class DiscountRate(TimeStamp):
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = 'discount_rates'
    
class ProductsDiscountRate(models.Model):
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount_rate = models.ForeignKey('DiscountRate', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_discount_rates'
        
class DetailImage(TimeStamp):
    detail_image_name = models.CharField(max_length=100)
    detail_image_url  = models.CharField(max_length=400)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)        

    class Meta:
        db_table = 'detail_images'
        
class Like(TimeStamp):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'likes'