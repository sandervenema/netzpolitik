from django.db import models
from django.utils import timezone

class Petition(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()

    def signatures(self):
        return self.signature_set.filter(active=True).count()


class Signature(models.Model):
    email = models.CharField(max_length=254, null=True)
    name = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=200, null=True)
    petition = models.ForeignKey(Petition)
    link = models.CharField(max_length=256, null=True)
    active = models.BooleanField(default=False)
    initial = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

