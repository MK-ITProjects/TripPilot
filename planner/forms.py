from django import forms

from config.forms import BootstrapFormMixin
from destinations.models import Destination
from .models import Expense, TripPlan


class TripPlanForm(BootstrapFormMixin, forms.Form):
    origin_city = forms.CharField(initial='Ahmedabad', max_length=120, label='Departure City')
    destination = forms.ModelChoiceField(queryset=Destination.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    travelers = forms.IntegerField(min_value=1, initial=2)
    trip_style = forms.ChoiceField(choices=TripPlan.STYLE_CHOICES, initial='mid')

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get('start_date'), cleaned.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError('End date must be after start date.')
        return cleaned


class AddStopForm(BootstrapFormMixin, forms.Form):
    destination = forms.ModelChoiceField(queryset=Destination.objects.all())
    arrival_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned = super().clean()
        arrival, departure = cleaned.get('arrival_date'), cleaned.get('departure_date')
        if arrival and departure and departure <= arrival:
            raise forms.ValidationError('Departure date must be after arrival date.')
        return cleaned


class BudgetCalculatorForm(BootstrapFormMixin, forms.Form):
    destination = forms.ModelChoiceField(queryset=Destination.objects.all())
    days = forms.IntegerField(min_value=1, initial=5)
    travelers = forms.IntegerField(min_value=1, initial=2)
    trip_style = forms.ChoiceField(choices=TripPlan.STYLE_CHOICES, initial='mid')


class ExpenseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'spent_on']
        widgets = {'spent_on': forms.DateInput(attrs={'type': 'date'})}
