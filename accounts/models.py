from datetime import datetime

from django.db import models
from django.utils import timezone



class data(models.Model):
    usedDate = models.DateTimeField('usedDate', default = datetime.now())
    item = models.CharField('Item', max_length=20)
    cost = models.IntegerField('cost')
    memo = models.CharField('memo', max_length = 500, blank = True)
    plan = models.BooleanField('plan')

    def __int__(self):
        return "%s %s %d %s %s" % (self.usedDate.strftime('%m/%d'),
                                         self.cost, self.item,
                                         self.memo)

    class Meta:
        get_latest_by = 'usedDate'
        ordering = ['usedDate']
        verbose_name = 'data'
        verbose_name_plural = verbose_name
    class Admin:
        pass
