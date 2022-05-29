from django import forms
from .models import Sample, SampleBulkUpload


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = "__all__"

    sampno = forms.CharField()


class SampleBulkUploadForm(forms.ModelForm):
    class Meta:
        model = SampleBulkUpload
        fields = ('csv_file',)
