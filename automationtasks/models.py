# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
import uuid
from django.contrib.postgres.fields import ArrayField, JSONField

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

ValidHostnameRegex1 = RegexValidator(
    r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$')

ValidHostnameRegex2 = RegexValidator(
    r'^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$')

ValidHostnameRegex = RegexValidator(
    r'^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$')


def f():
    d = uuid.uuid4()
    str = d.hex
    return str[0:10]


class automationSetting(models.Model):
    automationGlobal = models.CharField(blank=True, max_length=1024, default='disabled')
    automationProd = models.CharField(blank=True, max_length=1024, default='disabled')
    automationPreprod = models.CharField(blank=True, max_length=1024, default='disabled')
    automationTest = models.CharField(blank=True, max_length=1024, default='disabled')
    automationLab = models.CharField(blank=True, max_length=1024, default='disabled')
    gitRepolink = models.CharField(blank=True, max_length=1024)

    class Meta:
        db_table = "automationSetting"

    def __unicode__(self):
        return self.automationGlobal

    def __str__(self):
        return self.automationGlobal


# Automation Tasks type

class automationTaskType(models.Model):
    taskType = models.CharField(primary_key=True, max_length=255)
    gitTaskRepolink = models.CharField(blank=True, max_length=1024)

    class Meta:
        db_table = "automationTaskType"

    def __unicode__(self):
        return self.taskType

    def __str__(self):
        return self.taskType


# Automation Tasks table

class automationTasks(models.Model):
    taskId = models.CharField(primary_key=True, max_length=32, default=f)
    taskName = models.CharField(blank=True, max_length=32)
    taskNumber = models.CharField(blank=True, max_length=32)
    taskType = models.CharField(blank=True, max_length=255)
    taskTypelist = ArrayField(models.CharField(max_length=2000), blank=True, default=list)
    taskActionType = models.CharField(blank=True, max_length=255)
    taskDescription = models.CharField(blank=True, max_length=1024)
    taskCI = models.CharField(blank=True, max_length=1024)
    taskCIlist = ArrayField(models.CharField(max_length=2000), blank=True, default=list)
    taskNote = models.CharField(blank=True, max_length=1024)
    taskStatus = models.CharField(blank=True, max_length=255)
    taskRequester = models.CharField(blank=True, max_length=255)
    taskAssignee = models.CharField(blank=True, max_length=255)
    taskProject = models.CharField(blank=True, max_length=255)
    taskChangeticket = models.CharField(blank=True, max_length=255)
    taskTicketstatus = models.CharField(blank=True, max_length=255)
    taskConfigvars = JSONField(models.CharField(max_length=4000), blank=True, default=list)
    taskRundatetime = models.DateTimeField(blank=True, null=True)
    taskTicketrequired = models.CharField(blank=True, max_length=255)

    class Meta:
        db_table = "automationTasks"

    def __unicode__(self):
        return self.taskNumber

    def __str__(self):
        return self.taskNumber
