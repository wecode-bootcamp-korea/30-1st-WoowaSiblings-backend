from django.db   import models

from core.models import Time_stamp

class Batch(models.Model):
    batch = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'batches'

class User(Time_stamp):
    username     = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=300, blank=True)
    nickname     = models.CharField(max_length=100, blank=True)
    email        = models.CharField(max_length=100, unique=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True)
    address      = models.CharField(max_length=100, blank=True)
    zipcode      = models.CharField(max_length=100, blank=True)
    is_wecode    = models.BooleanField()
    point        = models.PositiveIntegerField(default=100000)
    batch        = models.ForeignKey('Batch', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'users'
        
class Wecode_user_detail(Time_stamp):
    thumbnail_image = models.CharField(max_length=400)
    selected_image  = models.CharField(max_length=400)
    status_message  = models.CharField(max_length=400)
    user            = models.OneToOneField('User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'wecode_user_details'


        
