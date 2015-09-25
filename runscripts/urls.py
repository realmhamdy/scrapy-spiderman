from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^home/$", views.HomeView.as_view(), name="runscripts_home"),
    url(r"^run/", views.RunScript.as_view(), name="runscripts_run")
]
