from pyroven import RavenConfig
from pyroven.pyroven_django import Raven
import django.contrib.auth as auth
from django.http import HttpResponse, HttpResponseRedirect
import os
import secret

# Configure everything beforehand
r = Raven()
if r.config is None:
    r.config = RavenConfig(os.path.join(secret.ABSPATH, "raven.ini"))

def rlogin(request):
    # Get the raven object and return a redirect to the raven server
    return r.get_login_redirect()

def rreturn(request):
    # Get the token which the raven server sent us - this should really
    # have a try/except around it to catch KeyError
    token = request.GET['WLS-Response']
    # See if this is a valid token
    user = auth.authenticate(response_str=token)
    if user is None:
        return HttpResponse("Raven did not return a username.")
    else:
        auth.login(request, user)
        return HttpResponseRedirect('/')
