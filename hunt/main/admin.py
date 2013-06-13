from django.contrib import admin
from main.models import *

class PageHitAdmin(admin.ModelAdmin):
    list_display = ('page', 'time', 'user')
    list_filter = ('user',)
    search_fields = ('page',)

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'text') 
    filter_horizontal = ('teams_read',)

class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('name', 'node')

class TeamPuzzleAdmin(admin.ModelAdmin):
    list_display = ('team', 'puzzle', 'description')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('team', 'judges', 'read', 'text')

class GuessAdmin(admin.ModelAdmin):
    list_display = ('puzzle', 'team', 'text', 'submitted', 'correct')
    list_filter = ('submitted', 'correct', 'team', 'puzzle')
    search_fields = ('text',)
    readonly_fields = ('pagehit',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','active','visible')
    filter_horizontal = ('members', 'puzzles_completed', 'nodes_visible')

class TokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'name')

admin.site.register(Token, TokenAdmin)
admin.site.register(Node)
admin.site.register(Hunt)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPuzzle, TeamPuzzleAdmin)
admin.site.register(Guess, GuessAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Message, MessageAdmin)
