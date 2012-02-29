from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'myproject.ridmap.views.index'),
    (r'^redirect/$', 'myproject.ridmap.views.redirect'), 
    (r'^maps/(?P<vote_vals>[\d\.-]+)/$', 'myproject.ridmap.views.projection'),
    (r'^maps/(?P<vote_vals>[\d\.-]+)/map.kmz', 'myproject.ridmap.views.getmap'),
    (r'^maps/(?P<vote_vals>[\d\.-]+)/style.kml', 'myproject.ridmap.views.mapstyle'),
    (r'^robots.txt$' , 'myproject.ridmap.views.robots'),
)
