from django import forms
from django.forms import Textarea, Select

from models import automationSetting, automationTasks, automationTaskType
from inventory.models import inventorydb

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

AUTOMATION_STATUS = (

    ('enabled', 'enabled'),
    ('disabled', 'disabled')

)

CHANGE_TICKET = (
    ('yes', 'yes'),
    ('no', 'no')
)

TASK_TYPE = (
    ('', ''),
    ('cisco-nxos-vlan-add', 'cisco-nxos-vlan-add'),
    ('cisco-nxos-generic-add', 'cisco-nxos-generic-add'),
    ('cisco-aci-epg-add', 'cisco-aci-epg-add'),
    ('cisco-aci-generic-add', 'cisco-aci-generic-add'),
    ('cisco-virl-generic', 'cisco-virl-generic'),
    ('juniper-srx-acl-add', 'juniper-srx-acl-add'),
    ('juniper-generic-add', 'juniper-generic-add'),
    ('cisco-generic-config-add', 'cisco-generic-config-add'),
    ('f5-generic-config-add', 'f5-generic-config-add'),
    ('f5-monitor-add', 'f5-monitor-add'),
    ('f5-node-add', 'f5-node-add'),
    ('edge-to-core-link-upgrade', 'edge-to-core-link-upgrade'),
    ('core-to-backbone-link-upgrade', 'core-to-backbone-link-upgrade'),
    ('server-task-install-updates', 'server-task-install-updates'),
    ('aws-ec2-generic', 'aws-ec2-generic'),
    ('aws-cloud-generic', 'aws-cloud-generic'),
    ('aws-vpc-generic', 'aws-vpc-generic'),
    ('azure-cloud-generic', 'azure-cloud-generic'),
    ('google-cloud-generic', 'google-cloud-generic'),
    ('rackspace-cloud-generic', 'rackspace-cloud-generic'),
    ('openstack-cloud-generic', 'openstack-cloud-generic'),
    ('vmware-cloud-generic', 'vmware-cloud-generic')
)


class EditAutomationSettings(forms.ModelForm):
    class Meta:
        model = automationSetting
        fields = '__all__'

        widgets = {
            'automationGlobal': Select(choices=AUTOMATION_STATUS),
            'automationProd': Select(choices=AUTOMATION_STATUS),
            'automationPreprod': Select(choices=AUTOMATION_STATUS),
            'automationTest': Select(choices=AUTOMATION_STATUS),
            'automationLab': Select(choices=AUTOMATION_STATUS)

        }


class AutomationTaskForm(forms.ModelForm):
    taskCI = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'chzn-select'}),
        queryset=inventorydb.objects.only('nodeName').filter(
            automationStatus='enabled'))

    taskType = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'chzn-select'}),
        queryset=automationTaskType.objects.only('taskType'))

    class Meta:
        model = automationTasks
        # fields = '__all__'
        fields = [
            "taskId",
            "taskName",
            "taskRequester",
            "taskType",
            "taskTypelist",
            "taskDescription",
            "taskCI",
            "taskCIlist",
            "taskProject",
            "taskConfigvars",
            "taskTicketrequired",
            "taskRundatetime"
        ]
        widgets = {
            "taskCIlist": forms.HiddenInput(),
            "taskTypelist": forms.HiddenInput(),
            "taskTicketrequired": Select(choices=CHANGE_TICKET)

        }


class editTaskForm(forms.ModelForm):
    class Meta:
        model = automationTasks
        fields = [
            "taskName",
            "taskTypelist",
            "taskDescription",
            "taskProject",
            "taskCIlist",
            "taskConfigvars",
            "taskTicketrequired",
            "taskRundatetime",
            "taskChangeticket",
            "taskAssignee",
            "taskStatus",
            "taskTicketstatus"
        ]
        widgets = {
            "taskTicketrequired": Select(choices=CHANGE_TICKET)

        }
