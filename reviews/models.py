from django.db import models

from core.models import TimeStamp

class Review(TimeStamp):
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    star_rating = models.PositiveIntegerField()
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'reviews'
        
class ReviewImage(TimeStamp):
    review_image_url = models.CharField(max_length=400)
    review           = models.ForeignKey('Review', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'review_images'
    