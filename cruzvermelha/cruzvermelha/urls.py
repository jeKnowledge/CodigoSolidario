from django.conf.urls import patterns, include, url
from RecHumanos.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from RecHumanos.views import *
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^contactos/$', contacto),
	url(r'^contactos/(?P<voluntario_id>\d+)/$', contacto),
	url(r'^editar_contacto/(?P<voluntario_id>\d+)/$', editar_contacto),
	url(r'^editar_disponibilidade/(?P<voluntario_id>\d+)/$', editar_disponibilidade),
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^login$', ulogin, name='login'),
    url(r'^dashboard$', dashboard, name='dashboard'),
    url(r'^logout$', quit, name='quit'),
    # url(r'^cruzvermelha/', include('cruzvermelha.foo.urls')),
    url(r'^avisos/(?P<desde>\d+)?/?$', listaAvisos),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
