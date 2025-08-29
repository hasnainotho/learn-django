from django.db import models

# Create your models here.
class TestModel(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    occupation = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.full_name