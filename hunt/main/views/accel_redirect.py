from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from main.models import Puzzle
from main.lib import test_puzzle_access
import re

@staff_member_required
def liveapi(request, path):
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = '/_liveapi/' + path
    return response

@login_required
def media(request, path):
    pid = int(re.split('/', path)[0])
    test_puzzle_access(request.user, Puzzle.objects.get(pk=pid))
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = '/_media/' + path
    return response
