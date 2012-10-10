import settings
import datetime
from main.models import Message
from main.views import get_team

def hunt(request):
    h = settings.HUNT
    h["now"] = datetime.datetime.now()
    # TODO Separate this out
    if request.user.is_staff:
        msgs = Message.objects.filter(read=False, judges=False).count() 
    elif request.user.is_authenticated():
        msgs = Message.objects.filter(read=False, judges=True, team=get_team(request.user)).count() 
    else:
        msgs = 0
    return {"hunt": h, "message_count": msgs}

