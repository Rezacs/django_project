from django.db import models
from solutions.models import Category
from users.models import Site , User
import uuid

class Announcement(models.Model):
    site = models.ForeignKey(Site , on_delete=models.DO_NOTHING , null=True , blank=True)
    category = models.ForeignKey(Category , on_delete=models.DO_NOTHING , null=True , blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default='Write something')
    owner = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    target = models.ForeignKey(User , related_name='target', on_delete=models.DO_NOTHING , null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField( blank=True , null=True)
    file = models.FileField(upload_to='announcement_file', blank=True , null=True)
    number = models.UUIDField(default=uuid.uuid4)
    def __str__(self) :
        return (self.title)
