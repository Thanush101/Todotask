# myapp/models.py

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('A', 'Must Do'),
        ('B', 'Should Do'),
        ('C', 'Nice to Do'),
        ('D', 'Delegate'),
        ('E', 'Eliminate'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    task_text = models.CharField(max_length=255)  # Task description
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='C')  # Priority based on ABCDE
    completed = models.BooleanField(default=False)  # Task completion status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the task was created

    def __str__(self):
        return self.task_text
