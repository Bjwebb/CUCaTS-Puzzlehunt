from django.views.generic import TemplateView, DetailView
from main.models import Puzzle, Team, Guess, TeamPuzzle
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from main.lib import get_team, test_puzzle_access
import Image, ImageDraw
import re

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from hunt import secret

class PuzzleView(DetailView):
    model = Puzzle

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, **kwargs):
        return super(PuzzleView, self).dispatch(request, **kwargs)

    def render_to_response(self, context):
        if 'xhr' in self.request.GET:
            return HttpResponse('', mimetype='application/javascript')
        else:
            return super(PuzzleView, self).render_to_response(context)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        test_puzzle_access(self.request.user, self.object)
        
        team = get_team(self.request.user)
        
        context = super(PuzzleView, self).get_context_data(**kwargs)
        guess_text = None
        if "guess" in self.request.POST:
            guess_text = self.request.POST["guess"]
        if "guess" in self.request.GET:
            guess_text = self.request.GET["guess"]
        if 'xhr' in self.request.GET:
            guess = Guess(puzzle=self.object,
                    team=team,
                    text=guess_text,
                    submitted=False,
                    pagehit = self.request.pagehit)
            guess.save()
            return []
        if guess_text:
            context['submitted'] = True
            if re.match("^"+self.object.solution+"$", guess_text):
                context['correct'] = True
                if team:
                    team.puzzles_completed.add(self.object)
            else:
                context['correct'] = False 
            guess = Guess(puzzle=self.object,
                    team=team,
                    text=guess_text,
                    submitted=True,
                    correct=context['correct'],
                    pagehit = self.request.pagehit)
            guess.save()

        context["completed"] = (
            self.request.user.is_staff
            or (self.object in team.puzzles_completed.all())
        )
        context["clue"] = None
        if context["completed"]: context["clue"] = self.object.clue
        
        context["teampuzzle"] = None
        if team:
            try:
                context["teampuzzle"] = TeamPuzzle.objects.get(
                    puzzle=self.object, team=team)
            except TeamPuzzle.DoesNotExist: pass
        return context

class PuzzlesView(TemplateView):
    template_name = "main/puzzles.html"
    puzzles_completed = None
    team = None
    @method_decorator(login_required)
    def dispatch(self, request, pk=None):
        if request.user.is_staff:
            if pk:
                self.team = Team.objects.get(pk=pk)
                self.puzzles_completed = self.team.puzzles_completed
            else:
                self.puzzles_completed = Puzzle.objects
                
        else:
            teams = request.user.team_set.all()
            if len(teams) > 0:
                self.puzzles_completed = teams[0].puzzles_completed
            else:
                raise PermissionDenied
        return super(PuzzlesView, self).dispatch(request, pk=pk)
        
    def get_context_data(self, **kwargs):
        out = []
        return {"puzzles": out, "team": self.team, "puzzles_pre": secret.puzzles_pre()}

from hunt.secret import puzzlesimg
