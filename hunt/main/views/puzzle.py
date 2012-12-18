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
class PuzzleView(DetailView):
    model = Puzzle
    template_name = "main/puzzle_detail.html"

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

        context["completed"] = self.request.user.is_staff or (self.object in team.puzzles_completed.all())
        context["clue"] = None
        if context["completed"]: context["clue"] = self.object.clue
        
        context["teampuzzle"] = None
        if team:
            try:
                context["teampuzzle"] = TeamPuzzle.objects.get(puzzle=self.object, team=team)
            except TeamPuzzle.DoesNotExist: pass
        return context

class PuzzlesView(TemplateView):
    template_name = "puzzles.html"
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
        out = [  ]
        # Contains a list of all the nodes in a current level
        level = [ -1, 0, -1 ]
        hadn7 = False
        while True:
            #try:
            #    if level[1] == -2:
            #        out.append(([[], [{"name": "You must complete two of the puzzles leading to this point."}], []], ""))
            #        break
            #except IndexError: pass
            node_placement = {}
            placement_i = 0
            i = 0
            connections = ""
            level_puzzles = []
            newlevel = []
            empty = True
            for node in level:
                if node == 7: hadn7 = True
                puzzles = Puzzle.objects.filter(fromnode=node).order_by("tonode")
                if len(puzzles) > 0: empty = False
                level_puzzles.append(list(puzzles))
                for puzzle in puzzles:
                    n = puzzle.tonode
                    incoming_puzzles = len( self.puzzles_completed.filter(tonode=n) )
                    if n not in node_placement:
                        if n==7 or n==14 or n==100:
                            if incoming_puzzles >= 1:
                                newlevel = [ -1, n, -1 ]
                            #elif incoming_puzzles >= 1:
                            #    newlevel = [ -1, -2, -1]
                            node_placement[n] = 1
                        else:
                            if incoming_puzzles >= 1:
                                newlevel.append(n)
                            else:
                                newlevel.append(-1)
                            node_placement[n] = placement_i
                            placement_i+=1
                    if puzzle in self.puzzles_completed.all():
                        thickness = "2"
                    else: thickness = "1"
                    connections += str(i)+str(node_placement[n])+thickness
                i+=1
                connections += "-"
            level = newlevel

            if empty:
                if hadn7 == False:
                    level = [ -1 , 100, -1 ]
                    hadn7 = True
                else: break
            out.append((level_puzzles, connections))
        return {"puzzles": out, "team": self.team}

def puzzlesimg(request, layout):
    img = Image.new("RGBA", (300,50))
    draw = ImageDraw.Draw(img)
    i=0
    c=0
    color = ["#AA0000", "#0000AA", "#009900", "#000000"]
    while i < len(layout):
        if layout[i] == "-":
            c=0
            i+=1
            continue
        draw.line([(50+100*int(layout[i]), 0), (50+100*int(layout[i+1]), 49)], fill=color[c], width=int(layout[i+2]))
        i+=3
        c+=1
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response

