from django.urls import path
from .views import ProductInventoryView, UpdateStockView, ReviewListView, ReviewModerationView, NotificationListView
from .views import MarkNotificationReadView, SendNotificationView, AdminActivityLogListView 

urlpatterns = [
    path('api/admin/inventory/', ProductInventoryView.as_view(), name='product-inventory'),

    path('api/admin/inventory/<int:product_id>/', UpdateStockView.as_view(), name='update-stock'),
    
    path('api/admin/reviews/', ReviewListView.as_view(), name='fetch-reviews'),
    path('api/admin/reviews/<int:review_id>/status/', ReviewModerationView.as_view(), name='moderate-review'),
 

    path('api/admin/notifications/', NotificationListView.as_view(), name='fetch-notifications'),
    path('api/admin/notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('api/admin/notifications/send/', SendNotificationView.as_view(), name='send-notifications'),

    path('api/admin/activity-log/', AdminActivityLogListView.as_view(), name='fetch-activity-logs')
]