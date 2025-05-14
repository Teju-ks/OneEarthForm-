from django.db import models
from django.contrib.auth.models import User


class Buyer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Seller(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return self.username
    

 
 

class ProductSale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_sales")
    product_type = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()  # Quantity in kilograms
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)  # Price per kg in ₹
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2)  # Total earnings in ₹
    date_sold = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time of sale

    def __str__(self):
        return f"{self.seller.username} - {self.product_type} ({self.quantity} kg)"
    

 
 
class OrganicProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
  

    def __str__(self):
        return self.name


class OrganicManure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    

    def __str__(self):
        return self.name
    

 
class Order(models.Model):
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=50)  # e.g., 'manure' or 'product'
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product_name} ({self.quantity})"
    
