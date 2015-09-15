from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from webpanel.util import generate_models
from webpanel.models import Spider


class CollectSpidersCommand(BaseCommand):

    def handle(self, *args, **options):
        if getattr(settings, "SPIDER_DIRS", None) is None:
            raise ImproperlyConfigured("Required 'SPIDER_DIRS' setting undefined")
        # now I want to create a spider for each one found using find_spiders
        # you'll need to create their item models first at the current configuration
