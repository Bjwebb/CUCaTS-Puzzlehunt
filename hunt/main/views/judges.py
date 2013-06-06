from django import forms
from django.views.generic import FormView, TemplateView
from main.models import Puzzle, Team
import os, json
import settings

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['puzzle'] = forms.ChoiceField(choices=Puzzle.objects.values_list('id', 'name'))
        self.fields['file']  = forms.FileField()

class UploadFileView(FormView):
    template_name = 'main/upload.html'
    form_class = UploadFileForm

    @method_decorator(staff_member_required)
    def dispatch(self, request):
        return super(UploadFileView, self).dispatch(request)

    def get_context_data(self, **context):
        if 'delete' in self.request.GET:
            puzzle_id = str(int(self.request.GET['puzzle']))
            f = self.request.GET['file']
            if '/' in f: raise Exception
            os.remove(os.path.join(settings.MEDIA_ROOT, puzzle_id, f))

        puzzles = dict((p.pk, p) for p in Puzzle.objects.all())
        files = []
        for d in os.listdir(settings.MEDIA_ROOT):
            try:
                files.append((puzzles[int(d)], os.listdir(os.path.join(settings.MEDIA_ROOT, d))))
            except ValueError:
                pass
        context['files'] = files
        return context

    def form_valid(self, form):
        puzzle_id = form.cleaned_data['puzzle']
        f = form.cleaned_data['file']
        folder = os.path.join(settings.MEDIA_ROOT, puzzle_id)
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(os.path.join(folder, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        context = super(UploadFileView, self).get_context_data(form=form)
        context['result'] = settings.MEDIA_URL+os.path.join(puzzle_id, f.name)
        return self.render_to_response(context)


class LiveView(TemplateView):
    template_name = "main/live.html"
    @method_decorator(staff_member_required)
    def dispatch(self, request):
        return super(LiveView, self).dispatch(request)
        
    def get_context_data(self, **kwargs):
        return {
            "puzzles_json": json.dumps(dict((x.pk, x.name) for x in Puzzle.objects.all())),
            "teams": Team.objects.all(),
            }

