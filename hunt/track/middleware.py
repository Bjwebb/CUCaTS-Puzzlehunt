from track.models import PageHit

class Log:
    def process_request(self, request):
        if request.user.is_authenticated():
            if not request.path.startswith('/track'):
                if 'xhr' in request.GET and 'ph' in request.GET:
                    ph = PageHit.objects.get(pk=request.GET['ph'])
                    if ph.user == request.user:
                        request.pagehit = ph
                        return None
                ph = PageHit(user=request.user, page=request.path)
                ph.save()
                request.pagehit = ph
                return None
