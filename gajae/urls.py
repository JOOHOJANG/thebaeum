"""gajae URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
#from django.contrib.auth import views as auth_views

from blog import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.signin, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'/'}),
    url(r'^class_apply/', views.classApply, name='class_apply'),
    url(r'^class_request/', views.request, name='class_request'),
    url(r'^friend_request/', views.friend_request, name='friend_request'),
    url(r'^signup/$', views.signup, name='signup'),
#    url(r'^match/(?P<index>\d+)/', views.match, name='match'),
    url(r'^post/(?P<index>\d+)/$',views.class_detail, name='class_detail'),
    url(r'^post/(?P<index>\d+)/edit/$',views.class_edit, name='class_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$',views.class_remove, name='class_remove'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)