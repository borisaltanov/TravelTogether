from django import forms
from .models import Travel
from accounts.models import Account


with open('travels/towns.txt') as infile:
    towns = infile.read().splitlines()

TOWNS = [(town, town) for town in towns]
DATE_FORMAT = ["%d.%m.%Y %H:%M", ]


class TravelForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=Account.objects.all(),
                                   widget=forms.HiddenInput(), required=False)
    depart_time = forms.DateTimeField(
        DATE_FORMAT,
        error_messages={'invalid': 'DateTime format is: dd.mm.yyyy hh:mm'})
    duration = forms.CharField(
        max_length=20, widget=forms.HiddenInput(), required=False)
    distance = forms.CharField(
        max_length=20, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Travel
        fields = ['owner', 'depart_time', 'start', 'end', 'free_seats', 'fee',
                  'duration', 'distance', ]
