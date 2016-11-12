from django import forms
from .models import Task
import datetime
# place form definition here
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['id','name','list_name','due_date','priority','state','description']
