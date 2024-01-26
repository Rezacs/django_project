import uuid
from django.db import models
from users.models import *
from solutions.models import Category
from solutions.models import *
import datetime
import time

class WorkRecord(models.Model):
    labor = models.ForeignKey(User,related_name='labor',on_delete=models.CASCADE)
    writer = models.ForeignKey(User,related_name='writer',on_delete=models.CASCADE , default=labor)
    verified = models.BooleanField(default=False)
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    # payed = models.BooleanField(default=False)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    length = models.TimeField(blank = True , null = True)
    length_minute = models.IntegerField(blank = True , null = True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return (f"{self.labor}-{self.date}")
    def save(self, *args, **kwargs):
        time1 = datetime.datetime.strptime(str(self.start),'%H:%M:%S')
        time2 = datetime.datetime.strptime(str(self.end),'%H:%M:%S')
        self.length = str(time2 - time1)
        hours, minutes, seconds = self.length.split(":")
        hours = int(hours)
        minutes = int(minutes)
        total_minutes = hours * 60 + minutes
        self.length_minute = total_minutes
        super(WorkRecord, self).save(*args, **kwargs)