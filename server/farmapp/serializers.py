from rest_framework import serializers
from .models import Product, Review, Notification, AdminActivityLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'farmer','productName', 'description', 'category', 'unitPrice','stockQuantity', 'productImage', 'status', 'createdAt','updatedAt']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewId', 'product', 'customer', 'rating', 'comment', 'rejectionReason', 'createdAt','updatedAt']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notificationId', 'message', 'type', 'createdDate', 'isRead', 'targetRole', 'targetUserId']

class AdminActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActivityLog
        fields = ['logId', 'adminId', 'action', 'targetId', 'timestamp']

