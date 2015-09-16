from __future__ import absolute_import
from celery import shared_task
import six
from twisted.internet import reactor, task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from .models import Spider, SpiderRun
from webpanel.util import enumerate_spider_classes


@shared_task
def start_spider(spider_id):
    # this is expected to hold up a celery worker until finished
    target_spider = Spider.objects.get(id=spider_id)
    spider_cls = [cls for proj, cls in enumerate_spider_classes() if cls.__name__ == target_spider.name][0]
    spider_run = SpiderRun.objects.create(spider=target_spider)
    spider_run.logfile.save("notused", six.StringIO())
    configure_logging({"LOG_FILE": spider_run.logfile.name})
    runner = CrawlerRunner()
    deferred = runner.crawl(spider_cls)
    deferred.addBoth(lambda _: reactor.stop())
    def check_stop_spider(runner, spider_run):
        if spider_run.stopped:
            spider_run.finish_reason = SpiderRun.FINISH_REASON_USER
            spider_run.save()
            runner.stop()
    periodic_stop_check = task.LoopingCall(check_stop_spider, runner, spider_run)
    periodic_stop_check.start(15, now=False)
    # attach the run id to the spider class. This will be used later in the saving pipeline
    setattr(spider_cls, "_run_id_", spider_run.id)
    reactor.run()
