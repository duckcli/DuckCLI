# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, HttpResponse
from models import inventorydb
from django.http import Http404, HttpResponseRedirect
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddNewNode, EditNode
import netaddr

from rest_framework import viewsets
from serializers import assetSerializer
from rest_framework.response import Response
from rest_framework import generics


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def asset_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = AddNewNode(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # External Script Updating /etc/hosts file with hostname & IPv/6 mapping
        hosts_name = form.cleaned_data['nodeName']
        hosts_MGMTIP = form.cleaned_data['mgmtIP']
        if netaddr.IPAddress(hosts_MGMTIP).version == 4:
            adresstype = 'ipv4'

        elif netaddr.IPAddress(hosts_MGMTIP).version == 6:
            adresstype = 'ipv6'

        # Save form data into Database-model
        instance.save()

        messages.success(request, "Successfully Created")
        # Redirect to main Inventory url
        return HttpResponseRedirect('/inventory/')
    context = {
        "form": form,
    }
    return render(request, "inventory_form.html", context)


@login_required
def asset_update(request, devicename):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(inventorydb, nodeName=devicename)
    form = EditNode(request.POST or None, instance=instance)
    form.fields['nodeName'].widget.attrs['readonly'] = True

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Asset</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect('/inventory/')

    context = {
        "title": instance.nodeName,
        "instance": instance,
        "form": form,
    }
    return render(request, "inventory_form.html", context)


# ### Below code will load inventory DB #####################

@login_required
def loadinventory(request):
    # load Inventory DB
    inventorylist = []
    inventroyall = inventorydb.objects.all()

    cisco_y = 0
    juniper_y = 0
    arista_y = 0
    unknown_y = 0
    for assetobj in inventroyall:

        inventorylist.append(
            [str(assetobj.nodeName), str(assetobj.model), str(assetobj.softwareVersion),
             str(assetobj.mgmtIP),
             str(assetobj.manufacturer), str(assetobj.adminStatus), str(assetobj.deviceGroup),
             str(assetobj.deviceType), str(assetobj.rackLocation), str(assetobj.site)])
        if assetobj.manufacturer.capitalize() == 'Cisco':
            cisco_y += 1
        elif assetobj.manufacturer.capitalize() == 'Juniper':
            juniper_y += 1
        elif assetobj.manufacturer.capitalize() == 'Arista':
            arista_y += 1
        else:
            unknown_y += 1

    # print cisco_y
    # print juniper_y
    # print unknown_y
    vendordata = [{'name': 'Cisco', 'y': cisco_y, 'drilldown': 'Cisco'},
                  {'name': 'Juniper', 'y': juniper_y, 'drilldown': 'Juniper'},
                  {'name': 'Arista', 'y': arista_y, 'drilldown': 'Arista'},
                  {'name': 'unknown', 'y': unknown_y, 'drilldown': 'null'}]

    return render(request, 'inventory.html',
                  {'inventorydata': inventorylist, 'vendorchartdata': vendordata})


@login_required
def loaddeviceinfo(request, hostname):
    try:
        if inventorydb.objects.get(nodeName=hostname).nodeName == hostname:
            deviceobject = inventorydb.objects.get(nodeName=hostname)
            devicefactslist = []
            devicefactslist.append(
                [str(deviceobject.nodeName), str(deviceobject.manufacturer),
                 str(deviceobject.deviceType), str(deviceobject.site), str(deviceobject.rackLocation)])

            devicefactsdist = {'hostname': deviceobject.nodeName, 'vendor': deviceobject.manufacturer,
                               'hardware': deviceobject.deviceType, 'sitename': deviceobject.site,
                               'racklocation': deviceobject.rackLocation, 'mgmtip': deviceobject.mgmtIP,
                               'configfile': deviceobject.currentConfig}

            int_stat_dataset = []

            instance = get_object_or_404(inventorydb, nodeName=hostname)
            form = EditNode(request.POST or None, instance=instance)
            form.fields['nodeName'].widget.attrs['readonly'] = True
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, "<a href='#'>Asset</a> Saved", extra_tags='html_safe')
                return HttpResponseRedirect('/inventory/%s' % hostname)

            vendorid = deviceobject.manufacturer
            # print vendorid
            # render view data
            return render(request, 'inventory_detail.html',
                          {'devfacts': devicefactslist, 'hostname': hostname, 'devfactdict': devicefactsdist,
                           'interface_status': int_stat_dataset, 'vendorinfo': vendorid,
                           'form': form})
    except inventorydb.DoesNotExist:
        raise Http404("Hostname does not exist in the Database")


class assetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows inventory assets to be viewed.
    """
    queryset = inventorydb.objects.all()
    serializer_class = assetSerializer


class assetView(generics.ListAPIView):
    serializer_class = assetSerializer

    def get_queryset(self):
        """
        This view should return a single asset determined by the hostname portion of the URL.
        GET /inventory/api/<xx-hostname-xx>/
        """
        hostname = self.kwargs['hostname']
        return inventorydb.objects.filter(nodeName=hostname)
