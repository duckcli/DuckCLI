from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.loadautomation, name='automation'),
    url(r'^createtask/$', views.create_tasks, name='createtask'),
    url(r'^api/$', (views.tasksViewSet.as_view({'get': 'list'})), name='apitaskslist'),
    url(r'^api/(?P<taskid>.*?)/$', (views.taskView.as_view()), name='apitaskview'),
    url(r'^(?P<taskid>.*?)/$', views.loadtaskinfo, name='taskpage')

]
