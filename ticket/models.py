import uuid
from django.db import models
from users.models import *
from solutions.models import Category
from solutions.models import *


class Ticket(models.Model):
    status_choices = (
        ('Active' , 'Active'),
        ('Completed', 'Completed'),
        ('Pending' , 'Pending'),
    )
    mode_choices = (
        ('Incident' , 'Incident'),
        ('New Service', 'New Service'),
    )
    number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True , blank=True)
    ticket_status = models.CharField(max_length=15 , choices=status_choices)
    solver = models.ForeignKey(User , related_name='solver',on_delete=models.SET_NULL, null=True , blank=True )
    site = models.ForeignKey(Site ,on_delete=models.SET_NULL, null=True , blank=True )
    category = models.ForeignKey(Category ,on_delete=models.SET_NULL, null=True , blank=True )
    solution = models.ForeignKey(Solution , on_delete=models.SET_NULL, null=True , blank=True)
    def __str__(self) :
        return self.title


