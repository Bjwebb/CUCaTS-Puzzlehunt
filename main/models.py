from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Puzzle(models.Model):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="", blank=True)
    fromnode = models.IntegerField(default=0)
    tonode = models.IntegerField(default=0)
    solution = models.CharField(max_length=256, default="", blank=True)

    # Used for serving slightly different puzzle information to different teams
    teams = models.ManyToManyField('Team', through='TeamPuzzle')
    # Clue for following puzzles
    clue = models.TextField(default="", blank=True)
    
    def __str__(self):
        return self.name

    
class Team(models.Model):
    name = models.CharField(max_length=256)
    members = models.ManyToManyField(User)
    puzzles_completed = models.ManyToManyField(Puzzle, blank=True)
    score1 = models.CharField(max_length=10, default='')
    score2 = models.CharField(max_length=10, default='')
    
    def __str__(self):
        return self.name

class TeamPuzzle(models.Model):
    team = models.ForeignKey(Team)
    puzzle = models.ForeignKey(Puzzle)
    description = models.TextField(default="", blank=True)

class Guess(models.Model):
    puzzle = models.ForeignKey(Puzzle)
    team = models.ForeignKey(Team)
    text = models.CharField(max_length=256) 
    time = models.DateTimeField(auto_now_add=True)

class Announcement(models.Model):
    title = models.CharField(max_length=256, default="")
    text = models.TextField(default="", blank=True) 
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time)+" . . . . . "+self.title

class Message(models.Model):
    team = models.ForeignKey(Team)
    judges = models.BooleanField()
    read = models.BooleanField(default=False)
    text = models.TextField(default="", blank=True) 
    time = models.DateTimeField(auto_now_add=True)
