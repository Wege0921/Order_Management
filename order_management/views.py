from rest_framework import generics, viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from order_management.models import Profile, Customer, Driver, Admin, RegulatoryBody, Order, Assign, Schedule, CompletedOrder
from order_management.serializers import (
    UserSerializer, ProfileSerializer, CustomerSerializer, DriverSerializer,
    AdminSerializer, RegulatoryBodySerializer, OrderSerializer, AssignSerializer,
    ScheduleSerializer, CompletedOrderSerializer, CustomTokenObtainPairSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create a profile for the user
        profile_data = request.data.get('profile', {})
        Profile.objects.create(user=user, **profile_data)
        
        # Include the profile in the response
        profile = user.profile
        profile_data = ProfileSerializer(profile).data
        
        return Response({
            "message": "User registered successfully.",
            "user": UserSerializer(user).data,
            "profile": profile_data
        }, status=status.HTTP_201_CREATED)

# Login View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# Profile ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()  # Fetch all profiles
    serializer_class = ProfileSerializer

    # Optional: Restrict profiles to the authenticated user
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.filter(user=self.request.user)
        return Profile.objects.none()  # Return empty queryset if not authenticated

# Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Driver ViewSet
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

# Admin ViewSet
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

# RegulatoryBody ViewSet
class RegulatoryBodyViewSet(viewsets.ModelViewSet):
    queryset = RegulatoryBody.objects.all()
    serializer_class = RegulatoryBodySerializer

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Assign ViewSet
class AssignViewSet(viewsets.ModelViewSet):
    queryset = Assign.objects.all()
    serializer_class = AssignSerializer

# Schedule ViewSet
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

# CompletedOrder ViewSet
class CompletedOrderViewSet(viewsets.ModelViewSet):
    queryset = CompletedOrder.objects.all()
    serializer_class = CompletedOrderSerializer



class UserProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            # Return the profile of the authenticated user
            return self.request.user.profile
        except Profile.DoesNotExist:
            raise NotFound("Profile does not exist for this user.")

#----------------to make driver access his scheduled order-----

class DriverScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter schedules based on the authenticated driver's profile
        driver_profile = self.request.user.profile
        return Schedule.objects.filter(assign__driver__profile=driver_profile)

#----------------to allow the regulatorybody to download completed orders-----
from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import get_object_or_404

def download_completed_orders(request, regulatory_body_id):
    # Fetch the regulatory body
    regulatory_body = get_object_or_404(RegulatoryBody, id=regulatory_body_id)
    
    # Fetch all completed orders
    completed_orders = CompletedOrder.objects.all()

    # Create a new Excel workbook and add a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Completed Orders"

    # Add headers
    ws.append([
        "Order ID", "Item", "Quantity", "Unit Price", "Total Price",
        "Customer", "Driver", "Completed Date", "Completed Time"
    ])

    # Add data rows
    for order in completed_orders:
        ws.append([
            order.assign.order.id,
            order.assign.order.item,
            order.assign.order.quantity,
            order.assign.order.unit_price,
            order.assign.order.total_price,
            order.assign.order.customer.profile.user.get_full_name(),
            order.assign.driver.profile.user.get_full_name(),
            order.completed_date,
            order.completed_time,
        ])

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=completed_orders_{regulatory_body.name}.xlsx'
    
    # Save the workbook to the response
    wb.save(response)
    return response