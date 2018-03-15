"""DuckCLI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from home import views as homeview


urlpatterns = [
    url(r'^$', homeview.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^automationtasks/', include('automationtasks.urls')),
    #url(r'^changecontrol/', include('changecontrol.urls')),
    url(r'^inventory/', include('inventory.urls')),
]
