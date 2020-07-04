from django import forms
from .models import recommandation


class recommandationForm(forms.ModelForm):
    class Meta:
        model = recommandation
        fields = ['user', 'compName', 'sent', 'recieved', 'opens', 'clics', 'dateRecomendation', 'hour']
