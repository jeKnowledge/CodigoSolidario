from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from RecHumanos.views import *
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^contactos/$', 'RecHumanos.views.contacto'),
	url(r'^contactos/(?P<voluntario_id>\d+)$', 'RecHumanos.views.contacto'),
    # Examples:
    # url(r'^$', 'cruzvermelha.views.home', name='home'),
    # url(r'^cruzvermelha/', include('cruzvermelha.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
