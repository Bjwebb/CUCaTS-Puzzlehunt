from django.conf.urls.defaults import patterns, url
from questionnaire.views import QuestionnaireView, QuestionnaireSummaryView 
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', QuestionnaireView.as_view()),
    url(r'^thankyou$', TemplateView.as_view(template_name="questionnaire/thankyou.html")),
    url(r'^summary$', QuestionnaireSummaryView.as_view()),
)
