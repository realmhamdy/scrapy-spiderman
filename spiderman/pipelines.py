from .models import SpiderRun


class SaveItemPipeline(object):

    def process_item(self, item, spider):
        SpiderRun.objects.get(id=spider._run_id_).save_item(item)
        return item
