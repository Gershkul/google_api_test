from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('maptapp.urls')),  # Home Page router
    url(r'api/', include('maptapp.urls_api'))  # REST API router
]
