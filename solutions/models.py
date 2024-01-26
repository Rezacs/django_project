from django.db import models
from users.models import *
from django.utils.text import slugify
from users.models import Site

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True , blank=True , null=True)
    parent = models.ForeignKey("self" , on_delete=models.CASCADE,  blank=True , null=True )
    class Meta :
        ordering = ('title',)
        verbose_name_plural = 'Categories'
    def __str__(self) :
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

class Solution(models.Model):
    site = models.ForeignKey(Site , on_delete=models.SET_NULL , null=True , blank=True)
    visible = models.BooleanField(default=True)
    visible_to_all = models.BooleanField(default=True)
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True , blank=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='Write something')
    owner = models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True)
    last_viewed = models.DateTimeField(null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='solutions_file', blank=True , null=True)
    slug = models.SlugField(max_length=255, unique=True , blank=True , null=True)
    def __str__(self) :
        return (self.title + ' -- ' + self.category.title)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Solution, self).save(*args, **kwargs)



