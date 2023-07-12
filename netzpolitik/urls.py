from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'openletter/', include('petitions.urls')),
    re_path(r'openletter/i18n/', include('django.conf.urls.i18n')),
    re_path(r'openletter/admin/', admin.site.urls),
]
