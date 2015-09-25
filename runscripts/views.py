import subprocess
from os import path as pth
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse


class HomeView(TemplateView):

    template_name = "runscripts/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["scripts"] = apps.get_app_config("runscripts").found_scripts
        return context


class RunScript(View):

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        script_path = request.POST["script_path"]
        # avoid running arbitrary scripts from the machine
        # FIXME this allows still a script to do something like '> /etc/password'
        if not script_path in apps.get_app_config("runscripts").found_scripts:
            return Http404()
        cmdline_args = request.POST["cmdline_args"]
        subprocess.Popen(' '.join([script_path, cmdline_args]))
        messages.add_message(request, messages.SUCCESS, "Script '{}' is running...".format(pth.basename(script_path)))
        return HttpResponseRedirect(reverse("runscripts_home"))
