from django.views.generic import FormView, ListView
from django.contrib.auth.models import User
from main.models import Team, Message, Announcement
from django import forms
from main.lib import get_team

class HomeView(ListView):
    queryset = Announcement.objects.order_by('-time')

    def get(self, request):
        team = get_team(self.request.user)
        if team:
            for announcement in self.queryset.exclude(teams_read=team):
                announcement.teams_read.add(team)
        return super(HomeView, self).get(self, request)


class SignupForm(forms.Form):
    team_name = forms.CharField(max_length=256, required=False)
    player1 = forms.CharField(required=False)
    player2 = forms.CharField(required=False)
    player3 = forms.CharField(required=False)

class SignupView(FormView):
    template_name = 'main/signup.html'
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
        return super(SignupView, self).form_valid(form)


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
        context = super(MessagesView, self).get_context_data(**kwargs)
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
                message = Message(team=team,
                    text=request.POST["msg"],
                    judges=False) 
                message.save()
        return self.get(request) 
   



