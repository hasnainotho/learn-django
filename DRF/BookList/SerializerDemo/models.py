from django.db import models

# Create your models here.
class SerializerMenu(models.Model):
    title = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.CharField(max_length=300)
