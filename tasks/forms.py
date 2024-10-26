from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'categoria', 'documento', 'existe', 'importante']
        widgets= {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Escribir el titulo' }),
            'categoria': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Escribir la categoria'}),
            'documento': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre del documento'}),
            'existe': forms.CheckboxInput(attrs={'class':'form-check-input ms-auto'}), 
            'importante': forms.CheckboxInput(attrs={'class':'form-check-input ms-auto'}), 
                     
        }
    