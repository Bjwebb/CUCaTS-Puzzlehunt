from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django import forms
from django.views.decorators.csrf import csrf_exempt                                          
from django.views.generic import FormView, TemplateView, DetailView, ListView
from main.models import Puzzle, Team, Message, Announcement, Guess, TeamPuzzle
import settings
import Image, ImageDraw

import os, re, json, datetime
from main.lib import get_team, test_puzzle_access

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


@staff_member_required
def liveapi(request, path):
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = '/_liveapi/' + path
    return response

@login_required
def media(request, path):
    pid = int(re.split('/', path)[0])
    test_puzzle_access(request.user, Puzzle.objects.get(pk=pid))
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = '/_media/' + path
    return response


class SignupForm(forms.Form):
    team_name = forms.CharField(max_length=256, required=False)
    player1 = forms.CharField(required=False)
    player2 = forms.CharField(required=False)
    player3 = forms.CharField(required=False)

class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = '/signup/thankyou'

    def form_valid(self, form):
        team = Team(name=form.cleaned_data['team_name'])
        team.save()
        def add_player(username, team):
            if username: 
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username)
                    user.save()
                team.members.add(user)
        add_player(form.cleaned_data['player1'], team)
        add_player(form.cleaned_data['player2'], team)
        add_player(form.cleaned_data['player3'], team)
        return super(FormView, self).form_valid(form)



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
        solution = None
        if "solution" in self.request.POST:
            solution = self.request.POST["solution"]
        if "solution" in self.request.GET:
            solution = self.request.GET["solution"]
        if 'xhr' in self.request.GET:
            if team:
                guess = Guess(puzzle=self.object, team=team, text=solution, submitted=False)
                guess.save()
            return []
        if solution:
            if team:
                guess = Guess(puzzle=self.object, team=team, text=solution, submitted=True)
                guess.save()
            if re.match("^"+self.object.solution+"$", solution):
                context['solution'] = "Well done you solved this puzzle. See the new <a href=\"/puzzles/\">puzzles</a>."
                if team:
                        team.puzzles_completed.add(self.object)
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



class LiveView(TemplateView):
    template_name = "live.html"
    @method_decorator(staff_member_required)
    def dispatch(self, request):
        return super(LiveView, self).dispatch(request)
        
    def get_context_data(self, **kwargs):
        return {
            "puzzles_json": json.dumps(dict((x.pk, x.name) for x in Puzzle.objects.all())),
            "teams": Team.objects.all(),
            }





class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['puzzle'] = forms.ChoiceField(choices=Puzzle.objects.values_list('id', 'name'))
        self.fields['file']  = forms.FileField()

class UploadFileView(FormView):
    template_name = 'upload.html'
    form_class = UploadFileForm

    @method_decorator(staff_member_required)
    def dispatch(self, request):
        return super(UploadFileView, self).dispatch(request)

    def form_valid(self, form):
        puzzle_id = form.cleaned_data['puzzle']
        f = form.cleaned_data['file']
        folder = os.path.join(settings.MEDIA_ROOT,puzzle_id)
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(os.path.join(folder, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        context = super(UploadFileView, self).get_context_data(form=form)
        context['result'] = settings.MEDIA_URL+os.path.join(puzzle_id, f.name)
        return self.render_to_response(context)

