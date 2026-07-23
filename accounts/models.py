"""
accounts/models.py
Extends Django's built-in User model with delivery-related profile info,
instead of writing a full custom auth system from scratch.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    One-to-one extension of Django's auth User.
    Stores the delivery address & phone number so checkout can
    auto-fill them for returning customers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    is_staff_manager = models.BooleanField(
        default=False,
        help_text="Check this if the user should manage menu items & order statuses "
                   "from the restaurant admin dashboard."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal: automatically create a UserProfile the moment a new User is
    created, so we never have to remember to do it manually in views.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # ensure profile exists even for users created before this signal existed
        UserProfile.objects.get_or_create(user=instance)
