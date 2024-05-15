from django import forms
from utilities.forms import BootstrapMixin

from .models import ExtraFile

class ExtraFileUploadForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = ExtraFile
        fields = [ 'name', 'file', 'circuit' ]


