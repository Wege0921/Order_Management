from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order_management.views import (
    RegisterView, CustomTokenObtainPairView, ProfileViewSet, CustomerViewSet,
    DriverViewSet, AdminViewSet, RegulatoryBodyViewSet, OrderViewSet,
    AssignViewSet, ScheduleViewSet, CompletedOrderViewSet, UserProfileView, DriverScheduleViewSet, download_completed_orders
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'regulatory-bodies', RegulatoryBodyViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'assigns', AssignViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'completed-orders', CompletedOrderViewSet)
router.register(r'driver-schedules', DriverScheduleViewSet, basename='driver-schedules')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('regulatory-bodies/<int:regulatory_body_id>/download-completed-orders/',
        download_completed_orders,
        name='download_completed_orders'
    ),
    path('', include(router.urls)),
]