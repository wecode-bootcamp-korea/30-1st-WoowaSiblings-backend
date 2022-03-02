from django.db import models

from core.models import Core

class Review(Core):
    title   = models.CharField(max_length=100)
    content = models.TextField()
    star    = models.IntegerField()
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product =  models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'reviews'
        
class Review_image(Core):
    review_image_url = models.CharField(max_length=300)
    review           = models.ForeignKey('Review', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'review_images'
    