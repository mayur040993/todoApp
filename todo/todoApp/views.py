from django.views.generic import View
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import List,Task
from Account.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date,timedelta,datetime
from .forms import TaskForm

@login_required
def lists_view(request):
    """
    listing the lists created by user
    """
    try:
        lists_task=List.objects.filter(users__user=request.user)
    except:
        lists=""
    paginator = Paginator(lists_task, 7)
    page = request.GET.get('page')
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lists = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lists = paginator.page(paginator.num_pages)
    return render(request,"todoApp/appview.html",{"lists":lists})

@login_required
def task_list(request,list_id=None):
    """
    listing the task in particular list
    """
    start=(date.today()+timedelta(-30)).strftime('%Y/%m/%d')
    end=date.today().strftime('%Y/%m/%d')
    if request.POST and 'Delete' in request.POST:
        try:
            list_delete=dict(request.POST)['task_selected']
        except:
            list_delete=[]
        del_tasks=Task.objects.filter(pk__in=list_delete)
        if del_tasks is not None:
            if (request.user.is_superuser) or (request.user.user in User.objects.filter()):
                del_tasks.delete()
    elif request.POST :
        date_string=request.POST['range']
        start,end=date_string.split(' - ')
    s=start.replace('/','-')
    e=end.replace('/','-')
    tasks_list=Task.objects.filter(list_name=list_id,list_name__users__user=request.user,due_date__range=[s,e])
    paginator = Paginator(tasks_list, 7)
    page = request.GET.get('page')
    try:
        tasks= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks = paginator.page(paginator.num_pages)
    print tasks
    today=date.today()
    return render(request,"todoApp/taskview.html",{"tasks":tasks,"today":today,"list_id":list_id,"start":start,"end":end})

@login_required
def task_create(request,list_id):
    """
    Creating task on given list
    """
    form = TaskForm(request.POST or None)
    try:
        li=List.objects.get(pk=list_id,users=request.user.user)
    except:
        #raise when url hit by user is not valid
        raise Http404(" Sorry Page is invalid ")
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('task_list',args=[li.id]))
    return render(request,"todoApp/task_form.html",{'form':form ,'li':li})

@login_required
def task_edit(request,list_id,task):
    """
    Read Task information
    """
    try:
        li_name=List.objects.get(pk=list_id)
    except:
        raise Http404("Invalid Page")
    li_list=List.objects.filter(users=request.user.user)
    print li_list

    if li_name in li_list:
        task=get_object_or_404(Task,pk=task,list_name__users=request.user.user)
        form=TaskForm(request.POST or None, instance=task)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('task_list',args=[li_name.id]))
    return render(request,"todoApp/task_form.html",{'form':form ,'li':li_name,'view':0,'edit':1,'task':task})


@login_required
def task_view(request,list_id,task):
    """
    Read Task information
    """
    try:
        li_name=List.objects.get(pk=list_id)
    except:
        raise Http404("Invalid Page")
    li_list=List.objects.filter(users=request.user.user)
    if li_name in li_list:
        #check whether task is available or not
        task=get_object_or_404(Task,pk=task,list_name__users=request.user.user)
        form=TaskForm(request.POST or None, instance=task)
    return render(request,"todoApp/task_form.html",{'form':form ,'li':li_name,'view':1,'edit':0,'task':task})
