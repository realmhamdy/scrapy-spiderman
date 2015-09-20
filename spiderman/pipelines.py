import os.path as pth
from .models import SpiderRun


class SaveItemPipeline(object):

    def process_item(self, item, spider):
        SpiderRun.objects.get(id=spider._run_id_).save_item(item)
        return item


class FixRelativeDownloadedImagesPipeline(object):
    """
    This should be used after the ImagesPipeline in ITEM_PIPELINES setting
    """
    def process_item(self, item, spider):
        if not item.get("images"): return item
        images = item["images"]
        for image_info in images:
            if not pth.isabs(image_info["path"]):
                image_info["path"] = pth.join(spider.settings.get("IMAGES_STORE"), image_info["path"])
        return item
