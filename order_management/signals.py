from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assign, Schedule, CompletedOrder
from .models import Profile, Customer, Driver, Admin, RegulatoryBody

@receiver(post_save, sender=Profile)
def create_profile_role_instance(sender, instance, created, **kwargs):
    """
    Automatically create a Customer, Driver, Admin, or RegulatoryBody instance
    when a Profile is created with the corresponding role.
    """
    if created:
        if instance.role == 'CUSTOMER':
            Customer.objects.create(profile=instance)
        elif instance.role == 'DRIVER':
            Driver.objects.create(profile=instance)
        elif instance.role == 'ADMIN':
            Admin.objects.create(profile=instance)
        elif instance.role == 'REGULATORY':
            RegulatoryBody.objects.create(profile=instance, name=f"Regulatory Body for {instance.user.username}")

@receiver(post_save, sender=Profile)
def update_profile_role_instance(sender, instance, **kwargs):
    """
    Automatically update or create a Customer, Driver, Admin, or RegulatoryBody instance
    when a Profile's role is updated.
    """
    if instance.role == 'CUSTOMER':
        Customer.objects.get_or_create(profile=instance)
        # Delete other role instances if they exist
        Driver.objects.filter(profile=instance).delete()
        Admin.objects.filter(profile=instance).delete()
        RegulatoryBody.objects.filter(profile=instance).delete()
    elif instance.role == 'DRIVER':
        Driver.objects.get_or_create(profile=instance)
        # Delete other role instances if they exist
        Customer.objects.filter(profile=instance).delete()
        Admin.objects.filter(profile=instance).delete()
        RegulatoryBody.objects.filter(profile=instance).delete()
    elif instance.role == 'ADMIN':
        Admin.objects.get_or_create(profile=instance)
        # Delete other role instances if they exist
        Customer.objects.filter(profile=instance).delete()
        Driver.objects.filter(profile=instance).delete()
        RegulatoryBody.objects.filter(profile=instance).delete()
    elif instance.role == 'REGULATORY':
        RegulatoryBody.objects.get_or_create(profile=instance, name=f"Regulatory Body for {instance.user.username}")
        # Delete other role instances if they exist
        Customer.objects.filter(profile=instance).delete()
        Driver.objects.filter(profile=instance).delete()
        Admin.objects.filter(profile=instance).delete()


@receiver(post_save, sender=Assign)
def create_schedule_for_assign(sender, instance, created, **kwargs):
    """
    Automatically create a Schedule instance when an Assign instance is created.
    """
    if created:
        # Create a Schedule instance linked to the Assign instance
        Schedule.objects.create(
            assign=instance,
            scheduled_date=instance.assigned_date,  # Use the assigned_date from Assign
            scheduled_time=instance.assigned_time,  # Use the assigned_time from Assign
            status=instance.status  # Use the status from Assign
        )



@receiver(post_save, sender=Schedule)
def create_completed_order_for_schedule(sender, instance, **kwargs):
    """
    Automatically create a CompletedOrder instance when a Schedule's status changes
    to 'Delivered to Customer' or 'Delivered to Team Leader'.
    """
    if instance.status in ['Delivered to Customer', 'Delivered to Team Leader']:
        # Check if a CompletedOrder instance already exists for this Assign instance
        if not CompletedOrder.objects.filter(assign=instance.assign).exists():
            # Create a CompletedOrder instance linked to the Assign instance
            CompletedOrder.objects.create(assign=instance.assign)