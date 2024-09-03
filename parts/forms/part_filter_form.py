from django import forms
from parts.models import Category

class PartFilterForm(forms.Form):
    part_name = forms.CharField(
        required=False,
        label='Part Name/Number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter part name/number'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Category',
        empty_label='Any Category',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
