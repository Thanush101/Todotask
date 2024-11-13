# myapp/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'priority']
        widgets = {
            'task_text': forms.TextInput(attrs={'placeholder': 'Enter your task'}),
            'priority': forms.Select(),
        }
