from django.conf.urls.defaults import patterns, url
from questionnaire.views import QuestionnaireView, QuestionnaireSummaryView 
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = patterns('',
    url(r'^$', QuestionnaireView.as_view(), name='questionnaire'),
    url(r'^thankyou$', TemplateView.as_view(template_name="questionnaire/thankyou.html")),
    url(r'^summary$', staff_member_required(QuestionnaireSummaryView.as_view())),
)
