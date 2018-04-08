"""myWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
import xadmin
from article.views import article, catlog, search
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^(g(?P<gid>\d*)/)?(p(?P<pid>\d*))?$', catlog),
    url(r'^g(?P<gid>\d+)/a(?P<aid>\d+)', article),
    url(r'^search(/p(?P<pid>\d*))?$', search, name='search'),
    url('^admin', xadmin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
