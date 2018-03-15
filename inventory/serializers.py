from models import inventorydb

from rest_framework import serializers


class assetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = inventorydb
        fields = (
        'nodeName', 'mgmtIP', 'manufacturer', 'make', 'connectProtocol', 'deviceType', 'operatingSystem', 'model',
        'site', 'rackLocation', 'softwareVersion')
