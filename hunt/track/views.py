from django.http import HttpResponse
from track.models import Event, PageHit
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

def add(request, ph_id, type):
    ph = PageHit.objects.get(pk=ph_id)
    if ph.user == request.user:
        e = Event(pagehit=ph, type=type) 
        e.save()
        return HttpResponse('', mimetype='application/javascript')
    else:
        raise PermissionDenied()
