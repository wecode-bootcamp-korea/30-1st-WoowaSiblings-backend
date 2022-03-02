from django.db   import models

from core.models import Time_stamp

class Categories(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'categories'
    
class Product(Time_stamp):
    name           = models.CharField(max_length=200)
    price          = models.DecimalField(max_digits=5, decimal_places=2)
    stock          = models.PositiveIntegerField()
    on_discount    = models.BooleanField()
    product_option = models.BooleanField()
    category       = models.ForeignKey('Categories', on_delete=models.CASCADE)
    service_detail = models.ForeignKey('Service_details', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products' 
        
class Product_time(Time_stamp):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    time    = models.ForeignKey('Time', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_time'

class Time(Time_stamp):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Times'
    
class Thumbnail_image(Time_stamp):
    thumbnail_image_url  = models.CharField(max_length=400)
    product              = models.OneToOneField('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'thumbnail_images'

class Service_detail(Time_stamp):
    content = models.CharField(max_length=400)
    
    class Meta:
        db_table = 'service_details'  
        
class Discount_rate(Time_stamp):
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = 'discount_rates'
    
class Products_discount_rate(models.Model):
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount_rate = models.ForeignKey('Discount_rate', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_discount_rates'
        
class Detail_image(Time_stamp):
    detail_image_name = models.CharField(max_length=100)
    detail_image_url  = models.CharField(max_length=400)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)        

    class Meta:
        db_table = 'detail_images'
        
class Like(Time_stamp):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'likes'