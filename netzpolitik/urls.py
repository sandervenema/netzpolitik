from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'openletter/', include('petitions.urls')),
    url(r'openletter/i18n/', include('django.conf.urls.i18n')),
    url(r'openletter/admin/', include(admin.site.urls)),
]
