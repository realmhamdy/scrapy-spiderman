from __future__ import absolute_import
from celery import shared_task
import six
import os
from twisted.internet import reactor, task
from scrapy.crawler import CrawlerRunner
from django.core.files import File
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from .models import Spider, SpiderRun
from spiderman.util import enumerate_spider_classes


@shared_task
def start_spider(spider_id):
    # this is expected to hold up a celery worker until finished
    target_spider = Spider.objects.get(id=spider_id)
    os.chdir(target_spider.project.path)  # to make get_project_settings work
    spider_cls = [cls for proj, cls in enumerate_spider_classes() if cls.name == target_spider.name][0]
    spider_run = SpiderRun.objects.create(spider=target_spider)
    spider_run.logfile.save("notused", File(six.StringIO()))
    configure_logging({"LOG_FILE": spider_run.logfile.name})
    runner = CrawlerRunner(get_project_settings())
    deferred = runner.crawl(spider_cls)

    def spiderrun_success_wrapper(spider_run):
        def handler():
            spider_run.finish_reason = SpiderRun.FINISH_REASON_FINISHED
            spider_run.save()
        return handler

    def spiderrun_fail_wrapper(spider_run):
        def handler():
            spider_run.finish_reason = SpiderRun.FINISH_REASON_FAILED
            spider_run.save()
        return handler

    deferred.addCallback(spiderrun_success_wrapper(spider_run))
    deferred.addErrback(spiderrun_fail_wrapper(spider_run))
    deferred.addBoth(lambda _: reactor.stop())

    def check_stop_spider(runner, run_id, task):
        if SpiderRun.objects.get(id=run_id).stopped:
            runner.stop()
            task.kw.pop("task").stop()
    periodic_stop_check = task.LoopingCall(check_stop_spider, runner, spider_run.id)
    periodic_stop_check.kw["task"] = periodic_stop_check  # allow my check access to the task to be able to stop it [hack]
    periodic_stop_check.start(15, now=False)
    # attach the run id to the spider class. This will be used later in the saving pipeline
    setattr(spider_cls, "_run_id_", spider_run.id)
    reactor.run()
