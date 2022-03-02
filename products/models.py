from django.db   import models

from core.models import Core

class Category(Core):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'categories'
    
class Product(Core):
    title          = models.CharField(max_length=200)
    main_image_url = models.CharField(max_length=300)
    price          = models.IntegerField()
    discount_price = models.IntegerField()
    discount_rate  = models.IntegerField()
    stock          = models.IntegerField()
    is_sale        = models.BooleanField()
    product_option = models.BooleanField()
    category       = models.ForeignKey('Categories', on_delete=models.CASCADE)
    service_detail = models.ForeignKey('Service_details', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products' 
        
class Product_option(Core):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    time    = models.ForeignKey('Time', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_options'

class Time(Core):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'times'
    
class Detail_image(Core):
    detail_image_name = models.CharField(max_length=100)
    detail_image_url  = models.CharField(max_length=300)
    product           = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'detail_images'

class Service_detail(Core):
    content = models.CharField(max_length=400)
    
    class Meta:
        db_table = 'service_details'    

class Like(Core):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'likes'