from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.loadinventory, name='inventory'),
    url(r'^createasset/$', views.asset_create, name='createasset'),
    url(r'^updateasset/(?P<devicename>.*?)/$', views.asset_update, name='editasset'),
    url(r'^api/$', (views.assetViewSet.as_view({'get': 'list'})), name='apipath'),
    url(r'^api/(?P<hostname>.*?)/$', (views.assetView.as_view()), name='apiassetview'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<hostname>.*?)/$', views.loaddeviceinfo, name='devicepage')

]
