from track.models import PageHit

class Log:
    def process_request(self, request):
        if not request.path.startswith('/track'):
            ph = PageHit(user=request.user, page=request.path)
            ph.save()
            request.pagehit_id = ph.pk
            return None
