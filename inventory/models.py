# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

ValidHostnameRegex1 = RegexValidator(
    r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$')

ValidHostnameRegex2 = RegexValidator(
    r'^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$')

ValidHostnameRegex = RegexValidator(
    r'^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$')


# Inventory DB table

class inventorydb(models.Model):
    nodeName = models.CharField(primary_key=True, max_length=255, validators=[ValidHostnameRegex])
    mgmtIP = models.GenericIPAddressField(max_length=1024)
    OOBTerminalServerConnector = models.CharField(blank=True, max_length=1024)
    OOBTerminalServerFQDN = models.CharField(blank=True, max_length=1024)
    OOBTerminalServerNodeName = models.CharField(blank=True, max_length=1024)
    OOBTerminalServerPort = models.CharField(blank=True, max_length=1024)
    OOBTerminalServerTCPPort = models.CharField(blank=True, max_length=1024)
    acls = models.CharField(blank=True, max_length=1024)
    adminStatus = models.CharField(max_length=1024)
    assetID = models.CharField(blank=True, max_length=1024)
    authMethod = models.CharField(blank=True, max_length=1024)
    barcode = models.CharField(blank=True, max_length=1024)
    budgetCode = models.CharField(blank=True, max_length=1024)
    budgetName = models.CharField(blank=True, max_length=1024)
    bulk_acls = models.CharField(blank=True, max_length=1024)
    operatingSystem = models.CharField(max_length=1024)
    connectProtocol = models.CharField(blank=True, max_length=1024)
    coordinate = models.CharField(blank=True, max_length=1024)
    deviceType = models.CharField(max_length=1024)
    enablePW = models.CharField(blank=True, max_length=1024)
    explicit_acls = models.CharField(blank=True, max_length=1024)
    gslb_master = models.CharField(blank=True, max_length=1024)
    implicit_acls = models.CharField(blank=True, max_length=1024)
    lastUpdate = models.DateTimeField(blank=True, null=True)
    layer2 = models.CharField(blank=True, max_length=1024)
    layer3 = models.CharField(blank=True, max_length=1024)
    layer4 = models.CharField(blank=True, max_length=1024)
    lifecycleStatus = models.CharField(blank=True, max_length=1024)
    loginPW = models.CharField(blank=True, max_length=1024)
    make = models.CharField(blank=True, max_length=1024)
    manufacturer = models.CharField(max_length=1024)
    model = models.CharField(blank=True, max_length=1024)
    onCallEmail = models.CharField(blank=True, max_length=1024)
    onCallID = models.CharField(blank=True, max_length=1024)
    onCallName = models.CharField(blank=True, max_length=1024)
    operationStatus = models.CharField(blank=True, max_length=1024)
    owner = models.CharField(blank=True, max_length=1024)
    owningTeam = models.CharField(blank=True, max_length=1024)
    projectID = models.CharField(blank=True, max_length=1024)
    projectName = models.CharField(blank=True, max_length=1024)
    room = models.CharField(blank=True, max_length=1024)
    serialNumber = models.CharField(blank=True, max_length=1024)
    site = models.CharField(blank=True, max_length=1024)
    currentConfig = models.TextField(blank=True, max_length=2000000)
    addNote = models.TextField(blank=True, max_length=1000000)
    hardwareEol = models.DateField(blank=True, null=True)
    softwareEol = models.DateField(blank=True, null=True)
    rackLocation = models.CharField(blank=True, max_length=1024)
    deviceFunction = models.CharField(blank=True, max_length=1024)
    deviceGroup = models.CharField(blank=True, max_length=1024)
    LocalLoginUser = models.CharField(blank=True, max_length=1024)
    softwareVersion = models.CharField(blank=True, max_length=1024)
    automationStatus = models.CharField(max_length=1024, default='disabled')

    class Meta:
        db_table = "inventorydb"

    def __unicode__(self):
        return self.nodeName

    def __str__(self):
        return self.nodeName
