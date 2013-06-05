from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from models import Hunt
import re

from main.lib import get_team

class LockDown:
    def process_request(self, request):
        try:
            HUNT = Hunt.objects.filter(active=True).values()[0]
            team = get_team(request.user)
            if HUNT["start"] > datetime.now():
                message = "This part of the site locked until the hunt begins."
            elif HUNT["end"] < datetime.now():
                message = "The hunt is now over, the site is locked until we announce results."
            elif team and not team.active:
                message = "Your team is currently disabled from viewing and solving puzzles. If this is unexpected please message the judges."
            else:
                return None
        except IndexError:
            message = "An error has occured, and the site is locked. Please inform the judges of this."
        
        if request.user.is_staff:
            return None
        else:
            if re.match("/$|/messages|/teams|/accounts", request.path):
                return None
            else:
                return render(request, "locked.html", {"text":message})

