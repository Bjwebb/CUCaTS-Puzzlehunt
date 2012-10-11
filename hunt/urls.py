from django.conf.urls.defaults import patterns, include, url
from hunt.main.views import HomeView, SignupView, PuzzleView, PuzzlesView, LiveView, MessagesView, UploadFileView
from django.views.generic import DetailView, ListView, RedirectView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from main.models import Puzzle, Team, Guess
from questionnaire.views import QuestionnaireView, QuestionnaireSummaryView 


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
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
    # url(r'^hunt/', include('hunt.foo.urls')),

    url(r'^q/$', QuestionnaireView.as_view()),
    url(r'^q/thankyou$', TemplateView.as_view(template_name="questionnaire/thankyou.html")),
    url(r'^q/summary$', QuestionnaireSummaryView.as_view()),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^upload$', UploadFileView.as_view()),
    url(r'^signup$', SignupView.as_view()),
    url(r'^signup/thankyou$', TemplateView.as_view(template_name="signup_thankyou.html")),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/puzzles/')),

)
