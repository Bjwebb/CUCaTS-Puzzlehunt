from django.db import models
from django.contrib.auth.models import User
from track.models import PageHit
import urllib2
import json

class Hunt(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    active = models.BooleanField(default=True)
    debriefed = models.BooleanField(default=False)

class Node(models.Model):
    def __unicode__(self):
        import secret
        return secret.node_name(self.id)

    def get_puzzle(self):
        try:
            return self.puzzle
        except Puzzle.DoesNotExist:
            return Puzzle(id=0, name='No puzzle')

class Puzzle(models.Model):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="", blank=True)
    scripts = models.TextField(default="", blank=True)
    node = models.OneToOneField(Node, null=True, blank=True)
    solution = models.CharField(max_length=256, default="", blank=True)
    quotes = models.TextField(default="", blank=True)
    nodes = models.TextField(default="", blank=True)
    show_solution_box = models.BooleanField(default=True)
    function = models.TextField(default="", blank=True)
    flag = models.BooleanField(default=False)

    # Used for serving slightly different puzzle information to different teams
    teams = models.ManyToManyField('Team', through='TeamPuzzle')
    
    def __unicode__(self):
        return self.name

    
class Team(models.Model):
    name = models.CharField(max_length=256)
    members = models.ManyToManyField(User)
    puzzles_completed = models.ManyToManyField(Puzzle, blank=True)
    nodes_visible = models.ManyToManyField(Node)
    score1 = models.CharField(max_length=10, default='', blank=True)
    score2 = models.CharField(max_length=10, default='', blank=True)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    achievements = models.TextField(default="", blank=True)
    
    def __unicode__(self):
        return self.name

class TeamPuzzle(models.Model):
    team = models.ForeignKey(Team)
    puzzle = models.ForeignKey(Puzzle)
    description = models.TextField(default="", blank=True)

class Guess(models.Model):
    class Meta:
        verbose_name_plural = 'guesses'
    puzzle = models.ForeignKey(Puzzle)
    team = models.ForeignKey(Team, null=True)
    text = models.CharField(max_length=256) 
    time = models.DateTimeField(auto_now_add=True)
    submitted = models.BooleanField(default=True)
    pagehit = models.ForeignKey(PageHit, null=True)
    correct = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        super(Guess,self).save(*args,**kwargs)
        try:
            urllib2.urlopen("http://127.0.0.1:8001/guess",
                    json.dumps([self.puzzle.pk,
                        (self.team.pk if self.team else -1),
                        self.text,
                        self.time.isoformat(),
                        self.submitted])
                    )
        except urllib2.URLError:
            pass

    def __unicode__(self):
        return self.text

class Announcement(models.Model):
    title = models.CharField(max_length=256, default="")
    text = models.TextField(default="", blank=True) 
    time = models.DateTimeField(auto_now_add=True)
    teams_read = models.ManyToManyField(Team, blank=True)

    def __unicode__(self):
        return unicode(self.time)+" . . . . . "+self.title

class Message(models.Model):
    class Meta:
        ordering = ['-time']

    team = models.ForeignKey(Team)
    judges = models.BooleanField()
    read = models.BooleanField(default=False)
    text = models.TextField(default="", blank=True) 
    time = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
    token = models.CharField(max_length=256, default="")
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="", blank=True)
