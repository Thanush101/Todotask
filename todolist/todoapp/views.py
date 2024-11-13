# tasks/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

# View for listing tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

# View for adding a task
@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        task_text = data.get('task_text', '')
        priority = data.get('priority', 'C')  # Default to 'C' if not provided

        if not task_text:
            return JsonResponse({'error': 'Task text is required'}, status=400)

        if priority not in ['A', 'B', 'C', 'D', 'E']:
            return JsonResponse({'error': 'Invalid priority value'}, status=400)

        # Create and save the task
        task = Task(task_text=task_text, priority=priority, user=request.user)
        task.save()
        return JsonResponse({
            'id': task.id,
            'task_text': task_text,
            'priority': task.get_priority_display(),
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# View for deleting a task
@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'message': 'Task deleted'})

# View for marking task as done
@csrf_exempt
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return JsonResponse({'message': 'Task marked as done'})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
        except Exception as e:
            return HttpResponse(f'Error: {e}')
    return render(request, 'register.html')

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')  # Redirect to your task list page after login
        else:
            return HttpResponse('Invalid username or password')
    return render(request, 'registration\login.html')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')