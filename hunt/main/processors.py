import settings
import datetime
from main.models import Message, Announcement, Hunt
from main.views import get_team

def hunt(request):
    try:
        h = Hunt.objects.filter(active=True).values()[0]
    except IndexError:
        h = {}
    h["now"] = datetime.datetime.now()
    # TODO Separate this out
    if request.user.is_staff:
        message_count = Message.objects.filter(read=False, judges=False).count() 
        announcement_count = 0
    elif request.user.is_authenticated():
        team = get_team(request.user) 
        message_count = Message.objects.filter(read=False, judges=True, team=team).count() 
        announcement_count = Announcement.objects.exclude(teams_read=team).count()
    else:
        message_count = 0
        announcement_count = 0
    return {"hunt": h,
            "message_count": message_count,
            "announcement_count": announcement_count }

