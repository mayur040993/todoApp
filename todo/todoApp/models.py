from __future__ import unicode_literals
from django.db import models
from Account.models import User
from datetime import date
from django.core.exceptions import ValidationError


class List(models.Model):
    """
    consist of list of tasks
    """
    name=models.CharField(max_length=255,null=False,blank=False)
    users = models.ForeignKey(User, null=True, on_delete=models.CASCADE,related_name='tasks')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % (self.name)

class Task(models.Model):
    """
    Denotes a todo Task
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    PRIORITY=(
        ('High','High'),
        ('Low','Low'),
        ('Medium','Medium'),
    )
    STATE=(
        ('Todo','Todo'),
        ('Doing','Doing'),
        ('Done','Done'),
    )
    description=models.TextField(null=False)
    priority = models.CharField(max_length=255, null=False, blank=False, choices=PRIORITY,default='Medium')
    state=models.CharField(max_length=255,null=False,blank=False,choices=STATE)

    list_name=models.ForeignKey(List,null=True,related_name='Lists')
    due_date=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.due_date<date.today():
            raise ValidationError("Wrong Due Date")
        if self.list_name==None:
            raise ValidationError("Please Select or create new list")

    def __unicode__(self):
        return "%s" % (self.name)
