"""keef URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

from downloaderApp.views import index, progress, status_page, cleanqueue, serveFile, \
    fileAndReturnIndex

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^serveFile/(?P<path>.*)$', serveFile, name='serveFile'),
    url(r'^status/(?P<job_id>.+)$', status_page, name='status_page'),
    url(r'^progress/(?P<job_id>.+)$', progress, name='progress'),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^cleanqueue/', cleanqueue, name='cleanqueue'),
    url(r'^finished/(?P<zipFile>.+)$', fileAndReturnIndex, name="fileAndReturnIndex"),
]
