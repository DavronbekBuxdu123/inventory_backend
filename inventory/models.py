from django.db import models

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=255)
    sku=models.CharField(max_length=100,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    current_stock=models.IntegerField(default=0) 

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

class StockMovement(models.Model):
    MOVEMENT_CHOICES=[
        ('IN','KIRIM'),
        ('OUT','CHIQIM')
    ]     
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='movements')
    quantity=models.PositiveIntegerField()
    movement_type=models.CharField(max_length=3,choices=MOVEMENT_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.movement_type} - {self.product.name} {self.quantity}"

