from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from .models import Product, Review, Notification, AdminActivityLog
from .serializers import ProductSerializer, ReviewSerializer, NotificationSerializer, AdminActivityLogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ProductInventoryView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        product_id = self.request.query_params.get('product_id')
        category = self.request.query_params.get('category')

        if product_id:
            queryset = queryset.filter(productId=product_id)
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        for product in queryset:
            if product.stockQuantity < 10:  # Threshold for low stock
                product.status = "low stock"
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class UpdateStockView(APIView):
    def put(self, request, product_id):
        try:
            product = Product.objects.get(productId=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        stock_quantity = request.data.get('stockQuantity')
        if stock_quantity is not None and int(stock_quantity) >= 0:
            product.stockQuantity = stock_quantity
            product.save()
            # Log activity here if logging is implemented
            return Response({"message": "Stock updated"}, status=status.HTTP_200_OK)
        

# For fetching all reviews
class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product_id')
        rating = self.request.query_params.get('rating')
        status = self.request.query_params.get('status')
        if product_id:
            queryset = queryset.filter(productId=product_id)
        if rating:
            queryset = queryset.filter(rating=rating)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

# For approving/rejecting reviews
class ReviewModerationView(APIView):
    def put(self, request, review_id):
        try:
            review = Review.objects.get(reviewId=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        status = request.data.get('status')
        if status in ["approved", "rejected"]:
            review.status = status
            review.save()
            return Response({"message": "Review status updated"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)


#fetch notification
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.all()
        is_read = self.request.query_params.get('isRead')
        notification_type = self.request.query_params.get('type')

        if is_read is not None:
            queryset = queryset.filter(isRead=is_read.lower() == 'true')
        if notification_type:
            queryset = queryset.filter(type=notification_type)
        return queryset
    
#Marked notification as read
class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, notification_id):
        try:
            notification = Notification.objects.get(notificationId=notification_id)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        notification.isRead = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
    
#Send notification to specific user
class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')
        target_role = request.data.get('targetRole')  # e.g., "admin", "farmer", "customer"
        target_users = request.data.get('targetUsers')  # List of user IDs

        if not message or not target_role:
            return Response({"error": "Message and target role are required"}, status=status.HTTP_400_BAD_REQUEST)

        if target_role == 'all':
            users = User.objects.all()
        elif target_users:
            users = User.objects.filter(id__in=target_users)
        else:
            users = User.objects.filter(groups__name=target_role)

        for user in users:
            Notification.objects.create(message=message, type="general", targetRole=target_role, targetUserId=user)

        return Response({"message": "Notifications sent successfully"}, status=status.HTTP_201_CREATED)
    

#Fetch Admin activity logs
class AdminActivityLogListView(ListAPIView):
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AdminActivityLog.objects.all()
        admin_id = self.request.query_params.get('adminId')
        action_type = self.request.query_params.get('action')
        start_date = self.request.query_params.get('startDate')
        end_date = self.request.query_params.get('endDate')

        if admin_id:
            queryset = queryset.filter(adminId=admin_id)
        if action_type:
            queryset = queryset.filter(action=action_type)
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        
        return queryset
    
#log admin action
def log_admin_action(admin, action, target_id):
    """
    Utility function to log admin actions.
    """
    AdminActivityLog.objects.create(
        adminId=admin,
        action=action,
        targetId=target_id,
    )


    

