from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Custom User Model with middle_name
class User(AbstractUser):
    middle_name = models.CharField(_("Middle Name"), max_length=100, blank=True, null=True)

class Profile(models.Model):
    ROLE_CHOICES = [
        ('CUSTOMER', _('Customer')),
        ('DRIVER', _('Driver')),
        ('ADMIN', _('Admin')),
        ('REGULATORY', _('Regulatory Body')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(_("Role"), max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    phone_number = PhoneNumberField(_("Phone Number"), region='ET')  # Ethiopian phone number format
    city = models.CharField(_("City"), max_length=100)
    sub_city = models.CharField(_("Sub City"), max_length=100)
    woreda = models.CharField(_("Woreda"), max_length=100)
    ketena = models.CharField(_("Ketena"), max_length=100)
    house_number = models.CharField(_("House Number"), max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Customer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name}"


class Driver(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='driver')
    license_number = models.CharField(_("License Number"), max_length=100)
    device_type = models.CharField(_("Device Type"), max_length=100)
    plate_number = models.CharField(_("Plate Number"), max_length=100)

    def __str__(self):
        return f"{self.profile.user.username} - {self.plate_number}"


class Admin(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return _("Admin: %(username)s") % {'username': self.profile.user.username}


class RegulatoryBody(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='regulatory_body')
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self):
        return _("Regulatory Body: %(name)s") % {'name': self.name}


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(_("Item"), max_length=100)
    measurement = models.CharField(_("Measurement"), max_length=50)
    quantity = models.PositiveIntegerField(_("Quantity"))
    unit_price = models.DecimalField(_("Unit Price"), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return _("Order #%(id)s - %(item)s") % {'id': self.id, 'item': self.item}


class Assign(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='assignment')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='assignments')
    assigned_date = models.DateField(_("Assigned Date"), auto_now_add=True)
    assigned_time = models.TimeField(_("Assigned Time"), auto_now_add=True)
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=[
            ('Scheduled', _('Scheduled')),
            ('In Transit', _('In Transit')),
            ('Delivered to Customer', _('Delivered to Customer')),
            ('Delivered to Team Leader', _('Delivered to Team Leader')),
        ],
        default='Scheduled'
    )

    def __str__(self):
        return _("Assign #%(id)s - %(item)s") % {'id': self.id, 'item': self.order.item}


class Schedule(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE, related_name='schedules')
    scheduled_date = models.DateField(_("Scheduled Date"))
    scheduled_time = models.TimeField(_("Scheduled Time"))
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=[
            ('Scheduled', _('Scheduled')),
            ('In Transit', _('In Transit')),
            ('Delivered to Customer', _('Delivered to Customer')),
            ('Delivered to Team Leader', _('Delivered to Team Leader')),
        ],
        default='Scheduled'
    )

    def __str__(self):
        return _("Schedule #%(id)s - %(item)s") % {'id': self.id, 'item': self.assign.order.item}


class CompletedOrder(models.Model):
    assign = models.OneToOneField(Assign, on_delete=models.CASCADE, related_name='completed_order')
    completed_date = models.DateField(_("Completed Date"), auto_now_add=True)
    completed_time = models.TimeField(_("Completed Time"), auto_now_add=True)

    def __str__(self):
        return _("Completed Order #%(id)s - %(item)s") % {'id': self.assign.id, 'item': self.assign.order.item}