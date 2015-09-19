import json
from django.views.generic import ListView, TemplateView, View
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Spider, SpiderRun
from .tasks import start_spider


class HomeView(ListView):

    template_name = "spiderman/home.html"
    model = Spider
    context_object_name = "spiders"


class StartSpiderView(View):
    """This creates a new SpiderRun
    """

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        spider_id = request.POST.get("id")
        target_spider = get_object_or_404(Spider, id=spider_id)
        if not target_spider.running:
            start_spider.delay(spider_id)
        if request.is_ajax():
            return HttpResponse(status=200)
        else:
            return HttpResponseRedirect(reverse("home"))


class RunStopView(View):

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        run_id = int(request.POST["run_id"])
        target_run = get_object_or_404(SpiderRun, id=run_id)
        target_run.stopped = True
        target_run.finish_time = timezone.now()
        target_run.finish_reason = SpiderRun.FINISH_REASON_USER
        target_run.save()
        if request.is_ajax():
            return HttpResponse(status=200)
        return HttpResponseRedirect(reverse("home"))


class RunLogView(TemplateView):

    template_name = "spiderman/runlog.html"

    def get(self, request, *args, **kwargs):
        run_id = int(self.kwargs["run_id"])
        target_run = get_object_or_404(SpiderRun, id=run_id)
        if request.is_ajax():
            return HttpResponse(content=target_run.logfile.read(), content_type="text/plain")
        return super(RunLogView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RunLogView, self).get_context_data(**kwargs)
        context["spider_run"] = get_object_or_404(SpiderRun, id=int(self.kwargs["run_id"]))
        return context


class RunItemsView(TemplateView):

    template_name = "spiderman/runitems.html"
    context_object_name = "run"

    def get(self, request, *args, **kwargs):
        target_run = self._get_run()
        if request.is_ajax():
            return HttpResponse(serializers.serialize("json", target_run.items.all()), content_type="application/json")
        return super(RunItemsView, self).get(request, *args, **kwargs)

    def _get_run(self):
        run_id = int(self.kwargs["run_id"])
        target_run = get_object_or_404(SpiderRun, id=run_id)
        return target_run

    def get_context_data(self, **kwargs):
        context = super(RunItemsView, self).get_context_data(**kwargs)
        context["run"] = self._get_run()
        # collect fieldnames of the [unknown] item model
        ITEM_MODEL = context["run"].get_item_model_class()
        context["fieldnames"] = [field.name for field in ITEM_MODEL._meta.get_fields(include_parents=False)]
        return context


class RunStatsView(View):

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        run_id = int(request.GET["run_id"])
        target_run = get_object_or_404(SpiderRun, id=run_id)
        data = dict()
        data["itemcount"] = target_run.items.count()
        data["logcount"] = target_run.logcount
        return HttpResponse(content=json.dumps(data), content_type="application/json")
