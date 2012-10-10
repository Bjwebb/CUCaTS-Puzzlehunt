from django.http import HttpResponse
from settings import HUNT
from datetime import datetime
from django.shortcuts import render
import re


class LockDown:
    def process_request(self, request):
        if HUNT["start"] > datetime.now():
            message = "This part of the site locked until the hunt begins."
        elif HUNT["end"] < datetime.now():
            message = "The hunt is now over, the site is locked until we announce results."
        else:
            return None
        
        if request.user.is_staff:
            return None
        else:
            if re.match("/$|/messages|/teams|/accounts", request.path):
                return None
            else:
                return render(request, "locked.html", {"text":message})

