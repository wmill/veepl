from django.db import models

# Create your models here.


class Riding(models.Model):
    ed_code = models.CharField(max_length=50)
    ed_name = models.CharField(max_length=200)
    victor  = models.CharField(max_length=3)
    blq = models.FloatField()
    cpc = models.FloatField()
    grn = models.FloatField()
    lpc = models.FloatField()
    ndp = models.FloatField()
    def __unicode__(self):
        return "%s (%s)" % (self.ed_code, self.ed_name)


