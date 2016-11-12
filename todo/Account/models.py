from __future__ import unicode_literals
from django.contrib.auth.models import User as user
from django.db.models.signals import post_save
from django.db import models

# Create your models here.
class User(models.Model):
    """
    Represents an user belonging to the organistaion
    """
    user = models.OneToOneField(user, null=False, blank=False, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=255, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    phone = models.IntegerField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "%s" % (self.user)

def create_user(sender, instance, created, **kwargs):
    """
    create a user when a django  user is created
    """
    user, created = User.objects.get_or_create(user=instance)
    user.name = instance.first_name
    user.email = instance.email
    user.save()

post_save.connect(create_user, sender=user)
