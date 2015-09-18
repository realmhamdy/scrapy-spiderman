from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r"^spiderman/", include("spiderman.urls")),
    url(r'^admin/', include(admin.site.urls))
]

urlpatterns += staticfiles_urlpatterns()
