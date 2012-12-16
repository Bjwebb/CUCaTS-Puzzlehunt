#!/usr/bin/python
from django.core.management import setup_environ
import settings
setup_environ(settings)
from main.models import Guess
import re
import datetime

scores = {}
puzzles = {}


for guess in Guess.objects.all():
    if guess.time > datetime.datetime(2012, 6, 16, 1, 50, 0) and guess.puzzle.pk in [3,10,11,13,12,26]: worth = 0.5
    else: worth = 1
    if guess.time > datetime.datetime(2012, 6, 16, 18, 0, 0) and (guess.puzzle.pk < 14 or guess.puzzle.pk == 26): worth = 0
    if re.match("^"+guess.puzzle.solution+"$", guess.text) and ( guess.team.name not in puzzles or not guess.puzzle.pk in puzzles[guess.team.name] ):
        try: scores[guess.team.name] += worth
        except KeyError: scores[guess.team.name] = worth
        
        if not guess.team.name in puzzles: puzzles[guess.team.name] = []
        puzzles[guess.team.name].append(guess.puzzle.pk)

for team,value in scores.items():
    print team,value

