# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, HttpResponse
from models import automationTasks, automationSetting
from inventory.models import inventorydb
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditAutomationSettings, AutomationTaskForm, editTaskForm
import netaddr
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from serializers import tasksSerializer
import json

import datetime


def datetime_handler(x):
    if isinstance(x, datetime.date):
        return x.isoformat()
    raise TypeError("Unknown type")


@login_required
def create_tasks(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = AutomationTaskForm(request.POST or None, initial={'taskRequester': request.user.username})
    form.fields['taskId'].widget.attrs['readonly'] = True
    form.fields['taskRequester'].widget.attrs['readonly'] = True

    if form.is_valid():
        instance = form.save(commit=False)
        # Save form data into Database-model
        task_cis = form.cleaned_data['taskCI']
        json_data = json.dumps(list(task_cis.values()), default=datetime_handler)
        ci_list_json = json.loads(json_data)
        ci_list = []
        for ci in ci_list_json:
            ci_list.append(ci['nodeName'])
        # instance.taskCI = ci_list
        instance.taskCIlist = ci_list
        task_type_list = form.cleaned_data['taskType']
        # print task_type_list
        instance.taskTypelist = list(task_type_list)
        instance.save()
        # form.save_m2m()
        messages.success(request, "Successfully Created")
        # Redirect to main Inventory url
        return HttpResponseRedirect('/')

    context = {
        "form": form,
    }
    return render(request, "task_form.html", context)


class tasksViewSet(viewsets.ModelViewSet):
    queryset = automationTasks.objects.all()
    serializer_class = tasksSerializer


class taskView(generics.ListAPIView):
    serializer_class = tasksSerializer

    def get_queryset(self):
        taskid = self.kwargs['taskid']
        return automationTasks.objects.filter(taskId=taskid)


@login_required
def loadautomation(request):
    # load automation tasks
    autotasklist = []
    allautotaks = automationTasks.objects.all()

    for tasks in allautotaks:
        autotasklist.append(
            [str(tasks.taskId), str(tasks.taskName), str(tasks.taskRequester),
             str(tasks.taskProject),
             str(tasks.taskRundatetime), str(tasks.taskAssignee), str(tasks.taskDescription)])

    return render(request, 'automation.html',
                  {'autotasklist': autotasklist})


@login_required
def loadtaskinfo(request, taskid):
    try:
        if automationTasks.objects.get(taskId=taskid).taskId == taskid:
            taskobject = automationTasks.objects.get(taskId=taskid)
            taskfactslist = []
            taskfactslist.append(
                [str(taskobject.taskId), str(taskobject.taskName), str(taskobject.taskRequester),
                 str(taskobject.taskProject),
                 str(taskobject.taskRundatetime), str(taskobject.taskAssignee), str(taskobject.taskDescription)])

            taskfactsdist = {'taskid': taskobject.taskId, 'taskname': taskobject.taskName,
                             'taskdesc': taskobject.taskDescription, 'taskassignee': taskobject.taskAssignee,
                             'taskproject': taskobject.taskProject, 'tasktequester': taskobject.taskRequester,
                             'taskruntime': taskobject.taskRundatetime, 'taskconfigvars': taskobject.taskConfigvars}

            instance = get_object_or_404(automationTasks, taskId=taskid)
            form = editTaskForm(request.POST or None, instance=instance)

            if form.is_valid():
                instance = form.save(commit=False)

                instance.save()
                messages.success(request, "<a href='#'>Task</a> Saved", extra_tags='html_safe')
                return HttpResponseRedirect('/automationtasks/%s' % taskid)

            return render(request, 'autotask_detail.html',
                          {'taskfacts': taskfactslist, 'taskid': taskid, 'taskfactdict': taskfactsdist,
                           'form': form})
    except automationTasks.DoesNotExist:
        raise Http404("Task does not exist in the Database")
