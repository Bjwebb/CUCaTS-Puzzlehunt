from django.conf.urls.defaults import patterns, url
from hunt.main.views import HomeView, SignupView, PuzzleView, PuzzlesView, LiveView, MessagesView, UploadFileView
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from main.models import Puzzle, Team, Guess

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'^messages/$', MessagesView.as_view()),
    url(r'^guesses/$', staff_member_required(ListView.as_view(queryset=Guess.objects.all().order_by("-time")))),
    url(r'^live/$', staff_member_required(LiveView.as_view())),
    url(r'^liveapi/(.*)$', 'main.views.liveapi'),
    url(r'^media/(.*)$', 'main.views.media'),
    url(r'^puzzles/$', PuzzlesView.as_view()),
    url(r'^puzzles/(?P<layout>.*).png$', "main.views.puzzlesimg"),
    url(r'^puzzles/(?P<pk>\d+)$', PuzzleView.as_view()),
    url(r'^teams/$', ListView.as_view(queryset=Team.objects.all().order_by("-score1"))),
    url(r'^teams/(?P<pk>\d+)$', staff_member_required(PuzzlesView.as_view())),
    url(r'^accounts/ravenlogin/$', 'main.views.raven_login', name='raven_login'),
    url(r'^accounts/ravenreturn/$', 'main.views.raven_return', name='raven_login'),

    url(r'^upload$', UploadFileView.as_view()),
    url(r'^signup$', SignupView.as_view()),
    url(r'^signup/thankyou$', TemplateView.as_view(template_name="signup_thankyou.html")),
)
