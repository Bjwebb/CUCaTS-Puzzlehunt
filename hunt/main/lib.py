from django.http import Http404

def test_puzzle_access(user, puzzle):
    if not user.is_staff:
        team = get_team(user)
        if team == None: raise Http404
        try:
            if not team.nodes_visible.filter(id=puzzle.node.id):
                raise Http404
        except Node.DoesNotExist:
            raise Http404

def get_team(user):
    if not hasattr(user, 'team_set'): # User might be anonymous 
        return None
    teams = user.team_set.all()
    if len(teams) > 0:
        return teams[0]
    else: return None
