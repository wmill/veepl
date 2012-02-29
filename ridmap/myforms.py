from django import forms

class VoteValueForm(forms.Form):
    blq = forms.FloatField()   
    cpc = forms.FloatField()
    grn = forms.FloatField()
    lpc = forms.FloatField()
    ndp = forms.FloatField()
    
