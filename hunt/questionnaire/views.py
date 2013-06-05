# Create your views here.
from django.forms import ModelForm, CharField
from questionnaire.models import *
from main.models import Puzzle, Hunt
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

class QuestionnaireForm(ModelForm):
    class Meta:
        model = Response
        exclude = ('response', 'user', 'time' )

from django.forms.models import inlineformset_factory

class QuestionnaireView(TemplateView):
    template_name = "questionnaire/response_form.html"

    def dispatch(self, request):
        if Hunt.objects.filter(active=True)[0].debriefed:
            return super(QuestionnaireView, self).dispatch(request)
        else:
            raise PermissionDenied

    def post(self, request):
        form = QuestionnaireForm(request.POST)
        response = form.save(commit=False)
        try:
            response.user = request.user
        except ValueError:
            pass
        response.save()
        PuzzleFormSet = inlineformset_factory(Response, PuzzleResponse)
        pfs = PuzzleFormSet(request.POST, instance=response)
        for form in pfs:
            form.save()
        return HttpResponseRedirect("/q/thankyou")
    
    def get_context_data(self):
        context = {}
        filled = False
        if self.request.user.is_authenticated():
            responses = Response.objects.filter(user=self.request.user).order_by("-time")
            if len(responses) > 0:
                filled = True
                context["form"] = QuestionnaireForm(instance=responses[0])
                PuzzleFormSet = inlineformset_factory(Response, PuzzleResponse, extra=0) 
                pfs = PuzzleFormSet(instance=responses[0])
                puzzles = [ ]
                for form in pfs.forms:
                    puzzles.append( Puzzle.objects.get(pk=form["puzzle"].value()) )
         
        if not filled:
            context["form"] = QuestionnaireForm()
            puzzles = Puzzle.objects.all().order_by('pk').values('pk','name')
            PuzzleFormSet = inlineformset_factory(Response, PuzzleResponse, extra=len(puzzles))
            pfs = PuzzleFormSet(initial=[ {'puzzle':x['pk'], 'name':x['name']} for x in puzzles ])
         
        context["formset"] = pfs
        context["forms"] = zip(pfs.forms, puzzles)
        return context

class QuestionnaireSummaryView(TemplateView):
    template_name="questionnaire/summary.html"

    def get_context_data(self):
        context = {}
        context["puzzles"] = Puzzle.objects.all()
        context["responses"] = PuzzleResponse.objects.all() 
        return context
