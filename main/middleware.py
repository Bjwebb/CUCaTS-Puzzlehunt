from django.http import HttpResponse
from settings import HUNT
from datetime import datetime
from django.shortcuts import render
import re

from main.views import get_team

class LockDown:
    def process_request(self, request):
        team = get_team(request.user)
        if HUNT["start"] > datetime.now():
            message = "This part of the site locked until the hunt begins."
        elif HUNT["end"] < datetime.now():
            message = "The hunt is now over, the site is locked until we announce results."
        elif team and not team.active:
            message = "Your team is currently disabled from viewing and solving puzzles. If this is unexpected please message the judges."
        else:
            return None
        
        if request.user.is_staff:
            return None
        else:
            if re.match("/$|/messages|/teams|/accounts", request.path):
                return None
            else:
                return render(request, "locked.html", {"text":message})

