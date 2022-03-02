from django.db   import models

from core.models import Core

class User(Core):
    nickname     = models.CharField(max_length=100)
    account      = models.CharField(max_length=100)
    password     = models.CharField(max_length=300)
    email        = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100)
    address      = models.CharField(max_length=100, blank=True)
    zipcode      = models.CharField(max_length=100, blank=True)
    point        = models.IntegerField()
    
    class Meta:
        db_table = 'users'
