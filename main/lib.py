def get_team(user):
    if not hasattr(user, 'team_set'): # User might be anonymous 
        return None
    teams = user.team_set.all()
    if len(teams) > 0:
        return teams[0]
    else: return None
