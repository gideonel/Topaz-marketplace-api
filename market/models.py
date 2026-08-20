from django.db import models

class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.IntegerField(default=0)
    category    = models.CharField(max_length=100, blank=True, default='')
    image       = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name
