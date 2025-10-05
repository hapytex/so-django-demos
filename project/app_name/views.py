from functools import cached_property

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, CreateView, DetailView

from app_name.forms import UploadForm, MatchFormSet
from app_name.models import ImportedFile
from app_name.resources import BookResource


# Create your views here.

class FileImportView(CreateView):
    model = ImportedFile
    fields = ['file', 'file_format']
    template_name = 'app_name/simple_form.html'

    def get_success_url(self):
        return reverse('file-match', kwargs={'pk': self.object.pk})

class MatchView(FormView):
    form_class = MatchFormSet
    target_resource = BookResource
    import_file_queryset = ImportedFile.objects.all()
    template_name = 'app_name/match_form.html'

    def get_success_url(self):
        return reverse('dry-run', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        import_file = self.import_file
        import_file.matching = form.cleaned_data
        import_file.save()
        return super().form_valid(form)

    @property
    def target_fields(self):
        return list(self.target_resource.fields)

    @cached_property
    def import_file(self):
        return self.import_file_queryset.get(pk=self.kwargs['pk'])

    def get_initial(self):
        return [{'target_column': t, 'source_column': None} for t in self.target_fields]

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['form_kwargs'] = {'source_column': [(h,h) for h in self.import_file.headers]}
        return kw

class DryRunView(DetailView):
    model = ImportedFile
    target_resource = BookResource

    def get_context_data(self, **kwargs):
        print(self.object.import_with(self.target_resource()))
        return super().get_context_data(**kwargs)

class RunView(FormView):
    pass