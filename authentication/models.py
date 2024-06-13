from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from content.models import Company
from django.dispatch import receiver
import uuid
import os

def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("profile",filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to=unique_filename,
                              null=True, blank=True)
    phone = models.TextField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Profile User : "+self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(models.signals.pre_save, sender=Profile) # sender - Specifies a particular sender to receive signals from.
def deleting_old_pic_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_picture = Profile.objects.get(pk=instance.pk).photo
            new_picture = instance.photo
            if old_picture and (old_picture.url != new_picture.url):
                old_picture.delete(save=False)
        except:
            pass

