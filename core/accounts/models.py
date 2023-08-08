from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from phone_field import PhoneField


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username


# creating profile after user registration (way 1)
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# creating profile after user registration (way 2)

# def save_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = Profile(user=kwargs['instance'])
#         user_profile.save()
#
#
# post_save.connet(save_profile, sender=User, )
