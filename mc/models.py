from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Config(models.Model):
    name = models.CharField(max_length=30)
    term = models.IntegerField()
    part = models.IntegerField()
    limit = models.IntegerField()
    # def __unicode__(self):
    #     return  u'%s %s' % (self.first_name,self.last_name)

class Decision(models.Model):
    # status 0 ,1,2
    financing_name = models.CharField(max_length=30)
    financing_term = models.IntegerField()
    financing_part = models.IntegerField()
    financing_type = models.CharField(max_length=2)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
    amount = models.IntegerField()
    interest = models.FloatField()
    status = models.IntegerField()