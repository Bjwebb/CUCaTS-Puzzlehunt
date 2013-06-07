#!/usr/bin/python
from django.core.management import setup_environ
import settings
setup_environ(settings)
from main.models import Node, Puzzle

for node in Node.objects.all():
    try:
        print node.puzzle
    except Puzzle.DoesNotExist:
        puzzle = Puzzle(name="Placeholder", solution="arstneio", node=node)
        puzzle.save()

