from django.db import models


class Job(models.Model):
    provider = models.CharField(max_length=255)

