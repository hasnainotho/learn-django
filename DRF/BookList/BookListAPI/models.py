from django.db import models

# Create your models here.
class BookList(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['published_date']
        verbose_name_plural = 'Book Lists'