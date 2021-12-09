from django import forms
from core.models import Process, Part


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Busca', max_length=100,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Busca'}))


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['number', 'process_class', 'subject', 'judge']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', }),
            'process_class': forms.TextInput(attrs={'class': 'form-control', }),
            'subject': forms.TextInput(attrs={'class': 'form-control', }),
            'judge': forms.TextInput(attrs={'class': 'form-control', }),
        }


PartFormSet = forms.modelformset_factory(
    Part,
    fields=('name', 'category'),
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'false'}),
        'category': forms.TextInput(attrs={'class': 'form-control', }),
    }, extra=0)
