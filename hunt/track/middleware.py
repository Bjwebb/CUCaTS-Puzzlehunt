from track.models import PageHit
from main.lib import get_team

class Log:
    def process_request(self, request):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        if not request.path.startswith('/track', '/liveapi'):
            if 'xhr' in request.GET and 'ph' in request.GET:
                ph = PageHit.objects.get(pk=request.GET['ph'])
                if ph.user == user:
                    request.pagehit = ph
                    return None
            ph = PageHit(user=user, team=get_team(user), page=request.path)
            ph.save()
            request.pagehit = ph
            return None
