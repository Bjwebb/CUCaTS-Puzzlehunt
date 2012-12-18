from django.conf.urls.defaults import patterns, url
from hunt.main.views import HomeView, SignupView, MessagesView
from hunt.main.views.puzzle import PuzzleView, PuzzlesView
from hunt.main.views.judges import LiveView, UploadFileView
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from main.models import Team, Guess

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^messages/$', MessagesView.as_view(), name='messages'),
    url(r'^signup$', SignupView.as_view()),
    url(r'^signup/thankyou$',
        TemplateView.as_view(template_name="main/signup_thankyou.html")),


    url(r'^liveapi/(.*)$', 'main.views.accel_redirect.liveapi'),
    url(r'^media/(.*)$', 'main.views.accel_redirect.media'),


    url(r'^puzzles/$', PuzzlesView.as_view(), name='puzzles'),
    url(r'^puzzles/(?P<layout>.*).png$',
        'main.views.puzzle.puzzlesimg',
        name='puzzlesimg'),
    url(r'^puzzles/(?P<pk>\d+)$', PuzzleView.as_view(), name='puzzle'),
    url(r'^teams/$',
        ListView.as_view(queryset=Team.objects.all().order_by("-score1")),
        name='teams'),
    url(r'^teams/(?P<pk>\d+)$',
        staff_member_required(PuzzlesView.as_view()),
        name='team'),
    url(r'^accounts/ravenlogin/$',
        'main.views.raven.rlogin',
        name='ravenlogin'),
    url(r'^accounts/ravenreturn/$',
        'main.views.raven.rreturn',
        name='ravenreturn'),


    url(r'^guesses/$',
        staff_member_required(
            ListView.as_view(
                queryset=Guess.objects.all().order_by("-time"))
            ),
        name='guesses'),
    url(r'^upload$', UploadFileView.as_view(), name='upload'),
    url(r'^live/$', LiveView.as_view(), name='live'),
)
