from django import forms
from .models import Travel
from accounts.models import Account


with open('travels/towns.txt') as infile:
    towns = infile.read().splitlines()

TOWNS = [(town, town) for town in towns]


class TravelForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=Account.objects.all(),
                                   widget=forms.HiddenInput(), required=False)
    depart_time = forms.DateTimeField(widget=forms.DateTimeInput())

    class Meta:
        model = Travel
        fields = ['owner', 'depart_time', 'start', 'end', ]
