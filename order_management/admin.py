from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from order_management.models import User, Profile, Customer, Driver, Admin, RegulatoryBody, Order, Assign, Schedule, CompletedOrder

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'middle_name', 'last_name')

# Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'city')

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('profile',)

# Driver Admin
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('profile', 'license_number', 'plate_number')

# Admin Admin
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('profile',)

# RegulatoryBody Admin
@admin.register(RegulatoryBody)
class RegulatoryBodyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name')

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'quantity', 'total_price')

# Assign Admin
@admin.register(Assign)
class AssignAdmin(admin.ModelAdmin):
    list_display = ('order', 'driver', 'status')

# Schedule Admin
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('assign', 'scheduled_date', 'scheduled_time', 'status')

# CompletedOrder Admin
@admin.register(CompletedOrder)
class CompletedOrderAdmin(admin.ModelAdmin):
    list_display = ('assign', 'completed_date', 'completed_time')

# Register the custom User model
admin.site.register(User, CustomUserAdmin)