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

def get_team(user):
    if not hasattr(user, 'team_set'): # User might be anonymous 
        return None
    teams = user.team_set.all()
    if len(teams) > 0:
        return teams[0]
    else: return None
