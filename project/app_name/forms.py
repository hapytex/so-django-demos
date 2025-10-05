import xdrlib
from django import forms
from django.forms import formset_factory
from import_export.formats.base_formats import DEFAULT_FORMATS

from app_name.source import Source, Constant

FORMAT_DICT = {x.CONTENT_TYPE: x() for x in DEFAULT_FORMATS if x().can_import()}

def combine_sources(source, constant):
    if source is not None:
        return Source(source)
    if constant:
        return Constant(constant)
    return None

class MatchRowForm(forms.Form):
    source_column = forms.TypedChoiceField(choices=(), empty_value=None, required=False)
    target_column = forms.CharField(widget=forms.HiddenInput())
    fixed_value = forms.CharField(required=False)

    def __init__(self, *args, source_column=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_column'].choices = [(None, '----'), *source_column]

class MatchFormSet(formset_factory(MatchRowForm, extra=0)):
    @property
    def cleaned_data(self):
        data = super().cleaned_data
        return {datum['target_column']: (datum['source_column'], datum['fixed_value']) for datum in data}

class UploadForm(forms.Form):
    imported_file = forms.FileField()
    format = forms.ChoiceField(
        label="Format",
        choices=[(x.CONTENT_TYPE, x.CONTENT_TYPE) for x in DEFAULT_FORMATS if x().can_import()],
    )

    def clean(self):
        data = super().clean()
        data['format'] = FORMAT_DICT.get(data['format'])
        return data