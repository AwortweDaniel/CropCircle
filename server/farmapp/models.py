from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from django.utils import timezone

# 1. User Model
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    passwordHash = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'User'


# 2. Farmer Model
class Farmer(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    farmerId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'farmer'})
    farmName = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    farmType = models.CharField(max_length=50)
    certifications = models.TextField(null=True, blank=True)
    verificationStatus = models.CharField(max_length=10, choices=VERIFICATION_STATUS_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.farmName 
    
    class Meta:
        db_table = 'Farmer'
        managed = False

# 3. Product Model
class Product(models.Model):
    PRODUCT_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('under_review', 'Under Review'),
    ]
    
    productId = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    productName = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    stockQuantity = models.IntegerField()
    productImage = models.ImageField(upload_to='product_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS_CHOICES, default='in_stock')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productName
    
    class Meta:
        db_table = 'Product'
        

# 4. Order Model
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    orderId = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    orderItems = models.JSONField()  # Store an array of products, including productId, quantity, and price
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.orderId
    
    class Meta:
        db_table = 'Order'
        

# 5. Cart Model (for Customers)
class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    items = models.JSONField()  # Store an array of items, including productId and quantity
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer
    
    class Meta:
        db_table = 'Cart'
        managed = False

# 6. Review Model
class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review {self.reviewId} - {self.product.productName}"

    
    class Meta:
        db_table = 'Review'
        

# 7. Admin Activity Log Model
class AdminActivityLog(models.Model):
    logId = models.AutoField(primary_key=True)
    adminId = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    action = models.CharField(max_length=255)
    targetId = models.IntegerField()  # ID of the target entity (e.g., farmerId or productId)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.action
    
    class Meta:
        db_table = 'AdminActivityLog'
    

#8. Notification Model
class Notification(models.Model):
    notificationId = models.AutoField(primary_key=True)
    message = models.TextField()
    type = models.CharField(max_length=50)  # e.g., "product submission", "review flag"
    createdDate = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)
    targetRole = models.CharField(max_length=50, null=True, blank=True)  # e.g., "admin", "farmer", "customer"
    targetUserId = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type} - {self.message[:30]}..."