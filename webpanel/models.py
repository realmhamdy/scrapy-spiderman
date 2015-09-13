from django.db import models


class Spider(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    running = models.BooleanField(default=False)
    runtime = models.DateTimeField(null=True, blank=True)
