from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from main.models import Puzzle, Team, Message, Announcement, Guess, TeamPuzzle
import datetime
import Image, ImageDraw

import re

from pyroven import RavenConfig
from pyroven.pyroven_django import Raven
def configure():
    r = Raven()
    if r.config is None:
        r.config = RavenConfig("/home/bjwebb/django/hunt/raven.ini")

def raven_login(request):
    # Ensure we're properly configured
    configure()
    # Get the raven object and return a redirect to the raven server
    r = Raven()
    return r.get_login_redirect()

def raven_return(request):
    # Ensure we're properly configured
    configure()

    # Get the token which the raven server sent us - this should really
    # have a try/except around it to catch KeyError
    token = request.GET['WLS-Response']
    # See if this is a valid token
    user = authenticate(response_str=token)
    if user is None:
        pass # Some sort of err
        return HttpResponse("balls")
    else:
        login(request, user)
        return HttpResponseRedirect('/')
    # Redirect somewhere sensible



def get_team(user):
    if not hasattr(user, 'team_set'): # User might be anonymous 
        return None
    teams = user.team_set.all()
    if len(teams) > 0:
        return teams[0]
    else: return None

from django.views.generic import ListView
class MessagesView(ListView):
    template_name = "main/message_list.html"
    model = Message
    def get_queryset(self):
        if self.request.user.is_staff:
            if 'team' in self.request.GET:
                self.team = Team.objects.get(pk=int(self.request.GET['team']))
            else:
                self.team = None
                queryset = Team.objects.extra(
                    select={'unread_message_count': 'SELECT COUNT(*) FROM main_message WHERE main_message.team_id=main_team.id AND main_message.read=false AND main_message.judges=false'})
                return queryset
        else:
            self.team = get_team(self.request.user) 
        queryset = self.model.objects.filter(team=self.team).order_by('time')
        if self.request.user.is_staff:
            queryset.filter(judges=False).update(read=True)
        else:
            queryset.filter(judges=True).update(read=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['team'] = self.team
        return context

    def post(self, request):
        if self.request.user.is_staff:
            team = Team.objects.get(pk=int(self.request.GET['team']))
            message = Message(team=team, text=request.POST["msg"], judges=True) 
            message.save()
        else:
            team = get_team(self.request.user)
            if team is not None:
                message = Message(team=team, text=request.POST["msg"], judges=False) 
                message.save()
        return self.get(request) 
   
class HomeView(ListView):
    template_name = "home.html"
    queryset = Announcement.objects.order_by('-time')

    def get(self,request):
        team = get_team(self.request.user)
        if team:
            for announcement in self.queryset.exclude(teams_read=team):
                announcement.teams_read.add(team)
        return super(HomeView, self).get(self, request)

from django.views.generic import DetailView
from django.http import Http404

def test_puzzle_access(user, puzzle):
    if not user.is_staff:
        team = get_team(user)
        if team == None: raise Http404
        # FIXME Doing this twice
        if puzzle.fromnode == 0: routes = [ 0 ]
        else: routes = team.puzzles_completed.filter(tonode=puzzle.fromnode)
        # Disable the double puzzle messages for now
        if False and (puzzle.fromnode == 7 or puzzle.fromnode == 14):
            if len(routes) < 2:
                raise Http404
        elif len(routes) < 1:
            raise Http404
 
class PuzzleView(DetailView):
    model = Puzzle
    template_name = "main/puzzle_detail.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PuzzleView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # FIXME Re-enable for live
        #test_puzzle_access(self.request.user, self.object)
        
        team = get_team(self.request.user)
        
        context = super(PuzzleView, self).get_context_data(**kwargs)
        solution = None
        if "solution" in self.request.POST:
            solution = self.request.POST["solution"]
        if "solution" in self.request.GET:
            solution = self.request.GET["solution"]
        if solution:
            if team:
                    guess = Guess(puzzle=self.object, team=team, text=solution)
                    guess.save()
            if re.match("^"+self.object.solution+"$", solution):
                context['solution'] = "Well done you solved this puzzle. See the new <a href=\"/puzzles/\">puzzles</a>."
                # FIXME Re-enable to make live
                #if team:
                #        team.puzzles_completed.add(self.object)
            else:
                context['solution'] = "Sorry, that is incorrect."
        context["completed"] = self.request.user.is_staff or (self.object in team.puzzles_completed.all())
        context["clue"] = None
        if context["completed"]: context["clue"] = self.object.clue
        
        context["teampuzzle"] = None
        if team:
            try:
                context["teampuzzle"] = TeamPuzzle.objects.get(puzzle=self.object, team=team)
            except TeamPuzzle.DoesNotExist: pass
        return context




from django.views.generic import TemplateView


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
            if teams > 0:
                self.puzzles_completed = teams[0].puzzles_completed
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


def choke(request):
    return HttpResponse("Wait and listen")

