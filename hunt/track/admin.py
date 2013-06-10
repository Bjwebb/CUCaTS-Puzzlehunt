from django.contrib import admin
from track.models import *

class PageHitAdmin(admin.ModelAdmin):
    list_display = ('page', 'time', 'user')
    list_filter = ('user',)
    search_fields = ('page',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('pagehit', 'time', 'type')
    readonly_fields = ('pagehit',)

admin.site.register(PageHit, PageHitAdmin)
admin.site.register(Event, EventAdmin)

