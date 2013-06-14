from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PageHit(models.Model):
    page = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,null=True)
    team = models.ForeignKey('main.Team',null=True)

    def __unicode__(self):
        return self.user.username+u' '+self.page

EVENTS = (
    ("T", "Tick"),
    ("F", "Focus"),
    ("B", "Blur")
)
class Event(models.Model):
    pagehit = models.ForeignKey(PageHit)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=2, choices=EVENTS)

