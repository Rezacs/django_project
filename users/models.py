import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import string
from django.contrib.auth import get_user_model

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Site(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True , blank=True , null=True)
    def __str__(self) :
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.name)
        super(Site, self).save(*args, **kwargs)

class User(AbstractUser):
    mode_choices = (
        ('engineer' , 'engineer'),
        ('customer', 'customer'),
    )
    is_customer = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    site = models.ForeignKey(Site ,on_delete=models.DO_NOTHING, null=True , blank=True)
    ssites = models.ManyToManyField(Site, related_name='ssites')
    contact = models.CharField(max_length=200,null=True , blank=True)
    image = models.ImageField(upload_to='profilepics', blank=True , null=True)
    def __str__(self) :
        return self.username
    
