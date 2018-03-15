from django import forms
from django.forms import Textarea, Select

from inventory.models import inventorydb

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

DEVICE_GROUP = (
    ('PROD', 'PROD'),
    ('PREPROD', 'PREPROD'),
    ('TEST', 'TEST'),
    ('LAB', 'LAB'),
    ('OTHER', 'OTHER')
)

DEVICE_TYPE = (

    ('ROUTER', 'ROUTER'),
    ('SWITCH', 'SWITCH'),
    ('FIREWALL', 'FIREWALL'),
    ('LOAD_BALANCER', 'LOAD_BALANCER',),
    ('CONTENT_SWITCH', 'CONTENT_SWITCH'),
    ('TERMINAL_SERVER', 'TERMINAL_SERVER'),
    ('LINUX_SERVER', 'LINUX_SERVER'),
    ('WINDOWS_SERVER', 'WINDOWS_SERVER'),
    ('OTHER', 'OTHER'),
    ('docker', 'docker'),
    ('IOT', 'IOT'),
    ('AWS-EC2-instance', 'AWS-EC2-instance')

)

ADMIN_STATUS = (

    ('PRODUCTION', 'PRODUCTION'),
    ('NON-PRODUCTION', 'NON-PRODUCTION'),
    ('OTHER', 'OTHER'),

)

CONNECTION_PROTOCOL = (
    ('NX-API', 'NX-API'),
    ('JUNOS-API', 'JUNOS-API'),
    ('F5-API', 'F5-API'),
    ('EOS-API', 'EOS-API'),
    ('SSH', 'SSH'),
    ('TELNET', 'TELNET'),
    ('NETCONF', 'NETCONF'),
    ('RESTAPI', 'RESTAPI'),
    ('RESTCONF', 'RESTCONF'),
    ('gRPC', 'gRPC'),
    ('SNMP', 'SNMP'),
    ('OTHER', 'OTHER')
)

VENDOR = (

    ('a10', 'A10 NETWORKS'),
    ('aruba', 'Aruba'),
    ('avocent', 'Avocent'),
    ('arista', 'ARISTA NETWORKS'),
    ('brocade', 'BROCADE'),
    ('cisco', 'CISCO SYSTEMS'),
    ('citrix', 'CITRIX'),
    ('dell', 'DELL'),
    ('foundry', 'FOUNDRY'),
    ('f5', 'F5'),
    ('force10', 'Force10'),
    ('juniper', 'JUNIPER'),
    ('mrv', 'mrv'),
    ('netscreen', 'NETSCREEN TECHNOLOGIES'),
    ('paloalto', 'Paloalto'),
    ('pica8', 'Pica8'),
    ('Ubuntu', 'Ubuntu'),
    ('Amazon', 'Amazon'),
    ('Google', 'Google'),
    ('Microsoft', 'Microsoft'),
    ('RedHat', 'RedHat'),
    ('Vmware', 'Vmware'),
    ('raspberryPi-iot', 'raspberryPi-iot'),
    ('arduino-iot', 'arduino-iot'),
    ('OTHER', 'OTHER')
)

AUTH_METHOD = (
    ('TACACS', 'TACACS'),
    ('LOCAL', 'LOCAL'),
    ('AD', 'AD'),
    ('LDAP', 'LDAP'),
    ('SSH-KEY', 'SSH-KEY'),
    ('OTHER', 'OTHER')

)

OPERATING_SYSTEMS = (
    ('IOS', 'IOS'),
    ('CATOS', 'CATOS'),
    ('NXOS', 'NXOS'),
    ('APIC', 'APIC'),
    ('JUNOS', 'JUNOS'),
    ('ARISTA-EOS', 'EOS'),
    ('F5-TMOS', 'TMOS'),
    ('A10-ACOS', 'ACOS'),
    ('LINUX', 'LINUX'),
    ('UNIX', 'UNIX'),
    ('WINDOWS', 'WINDOWS'),
    ('MAC', 'MAC'),
    ('ANDRIOD', 'ANDRIOD'),
    ('ARDUINO', 'ARDUINO'),
    ('RASPBIAN', 'RASPBIAN'),
    ('OTHER', 'OTHER')

)

AUTOMATION_STATUS = (

    ('enabled', 'enabled'),
    ('disabled', 'disabled')

)


class AddNewNode(forms.ModelForm):
    class Meta:
        model = inventorydb
        fields = [
            "deviceGroup",
            "deviceType",
            "adminStatus",
            "nodeName",
            "mgmtIP",
            "connectProtocol",
            "manufacturer",
            "model",
            "authMethod",
            "operatingSystem",
            "automationStatus",

        ]

        widgets = {
            'deviceGroup': Select(choices=DEVICE_GROUP),
            'deviceType': Select(choices=DEVICE_TYPE),
            'connectProtocol': Select(choices=CONNECTION_PROTOCOL),
            'manufacturer': Select(choices=VENDOR),
            'adminStatus': Select(choices=ADMIN_STATUS),
            'authMethod': Select(choices=AUTH_METHOD),
            'operatingSystem': Select(choices=OPERATING_SYSTEMS),
            'automationStatus': Select(choices=AUTOMATION_STATUS),

        }


class EditNode(forms.ModelForm):
    class Meta:
        model = inventorydb
        fields = '__all__'

        widgets = {
            'deviceGroup': Select(choices=DEVICE_GROUP),
            'deviceType': Select(choices=DEVICE_TYPE),
            'connectProtocol': Select(choices=CONNECTION_PROTOCOL),
            'manufacturer': Select(choices=VENDOR),
            'adminStatus': Select(choices=ADMIN_STATUS),
            'authMethod': Select(choices=AUTH_METHOD),
            'operatingSystem': Select(choices=OPERATING_SYSTEMS),
            'automationStatus': Select(choices=AUTOMATION_STATUS),

        }
