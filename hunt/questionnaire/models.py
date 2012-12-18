from django.db import models
from main.models import Puzzle
from django.contrib.auth.models import User

# Create your models here.

COMPETE = (
    ("YY", "Yes, remind me next year"),
    ("YN", "Yes, but I won't be here next year"),
    ("NN", "No")
)

class Response(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    most_interesting_puzzle = models.ForeignKey(Puzzle, related_name='response_most_interesting', blank=True, null=True)
    least_interesting_puzzle = models.ForeignKey(Puzzle, related_name='response_least_interesting', blank=True, null=True)
    length_of_puzzlehunt = models.CharField(max_length=1, choices=(("L","Too Long"),("A","About Right"),("S","Too Short")), blank=True)
    opinion_of_overall_structure = models.TextField(default="", blank=True)
    aspects_of_puzzles_you_liked = models.TextField(default="", blank=True)
    aspects_of_puzzles_you_disliked = models.TextField(default="", blank=True)
    website_suggestions = models.TextField(default="", blank=True)
    other_comments = models.TextField(default="", blank=True)
    would_you_compete_again = models.CharField(max_length=2, choices=COMPETE, default="", blank=True)

    def __unicode__(self): return unicode(self.user)

RATING_CHOICES = (
    (-1, ''),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class PuzzleResponse(models.Model):
    response = models.ForeignKey(Response)
    puzzle = models.ForeignKey(Puzzle)
    difficulty = models.IntegerField(default=-1, choices=RATING_CHOICES)
    interest = models.IntegerField(default=-1, choices=RATING_CHOICES)
    
    def __unicode__(self): return unicode(self.response.user)+u' '+unicode(self.puzzle)+u' '+str(self.interest)+u' '+str(self.difficulty)

