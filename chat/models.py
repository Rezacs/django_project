from django.db import models
from ticket.models import *
from dashboard.models import Announcement

class Chat(models.Model):
    ticket = models.ForeignKey(Ticket , on_delete=models.CASCADE )
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)
    def __str__(self) :
        return (self.ticket.title + ' -- ' + self.user.username)

class ChatAnnouncement(models.Model):
    announcement = models.ForeignKey(Announcement , on_delete=models.CASCADE )
    owner = models.ForeignKey(User , on_delete=models.CASCADE )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)
    def __str__(self) :
        return (self.owner.username + ' -- ' + self.announcement.title)
