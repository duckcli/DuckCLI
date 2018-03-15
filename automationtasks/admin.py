# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import automationSetting , automationTasks, automationTaskType

admin.site.register(automationSetting)
admin.site.register(automationTasks)
admin.site.register(automationTaskType)

