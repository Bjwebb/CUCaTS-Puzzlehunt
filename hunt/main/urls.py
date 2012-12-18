from django.conf.urls.defaults import patterns, url
from hunt.main.views import HomeView, SignupView, MessagesView
from hunt.main.views.puzzle import PuzzleView, PuzzlesView
from hunt.main.views.judges import LiveView, UploadFileView
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from main.models import Team, Guess

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'^messages/$', MessagesView.as_view()),
    url(r'^signup$', SignupView.as_view()),
    url(r'^signup/thankyou$', TemplateView.as_view(template_name="signup_thankyou.html")),

    url(r'^liveapi/(.*)$', 'main.views.accel_redirect.liveapi'),
    url(r'^media/(.*)$', 'main.views.accel_redirect.media'),

    url(r'^puzzles/$', PuzzlesView.as_view()),
    url(r'^puzzles/(?P<layout>.*).png$', "main.views.puzzle.puzzlesimg"),
    url(r'^puzzles/(?P<pk>\d+)$', PuzzleView.as_view()),
    url(r'^teams/$', ListView.as_view(queryset=Team.objects.all().order_by("-score1"))),
    url(r'^teams/(?P<pk>\d+)$', staff_member_required(PuzzlesView.as_view())),
    url(r'^accounts/ravenlogin/$', 'main.views.raven.rlogin'),
    url(r'^accounts/ravenreturn/$', 'main.views.raven.rreturn'),

    url(r'^guesses/$', staff_member_required(ListView.as_view(queryset=Guess.objects.all().order_by("-time")))),
    url(r'^upload$', UploadFileView.as_view()),
    url(r'^live/$', LiveView.as_view()),
)
