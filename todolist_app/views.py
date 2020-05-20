from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import Tasklist
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method =="POST":
        form=Taskform(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manager = request.user
            instance.save()
        messages.success(request,("New Task Added"))    
        return redirect('todolist')    

    else:
        all_task=Tasklist.objects.filter(manager=request.user)
        paginator=Paginator(all_task,5)
        page=request.GET.get('pg')
        all_task=paginator.get_page(page)
        return render(request,'todolist.html',{'all_task':all_task})
@login_required
def delete_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id) 
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request,("Access Restricted,You are not Allowed!!!"))        
    return redirect('todolist')  
@login_required
def edit_task(request,task_id):
    if request.method =="POST":
        task=Tasklist.objects.get(pk=task_id) 
        form=Taskform(request.POST or None,instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,("Task Editted"))    
        return redirect('todolist')    
    else:
        task_obj=Tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})
@login_required
def complete_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id) 
    if task.manager == request.user:
        task.done=True
        task.save()
    else:
        messages.error(request,("Access Restricted,You are not Allowed!!!"))            
    return redirect('todolist')  

def pending_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id) 
    if task.manager == request.user:
        task.done=False
        task.save()
    else:
        messages.error(request,("Access Restricted,You are not Allowed!!!"))
    return redirect('todolist')  
def index(request):
    contect={
        'index_text':"Welcome to Home Page",

        }

    return render(request,'index.html',contect)




def contact(request):
    contect={
        'contact_text':"Welcome to Contact Us Page",

        }

    return render(request,'contact.html',contect)

def about(request):
    contect={
        'about_text':"Welcome to About Us",

        }

    return render(request,'about.html',contect)

