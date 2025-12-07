from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ["nombre", "categoria", "descripcion", "estado", "ingresos", "gastos"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input", "placeholder": "Nombre"}),
            "categoria": forms.TextInput(attrs={"class": "input", "placeholder": "Categoría"}),
            "descripcion": forms.Textarea(attrs={"class": "textarea", "rows": 3, "placeholder": "Descripción"}),
            "estado": forms.Select(attrs={"class": "input"}),
            "ingresos": forms.NumberInput(attrs={"class": "input", "step": "0.01"}),
            "gastos": forms.NumberInput(attrs={"class": "input", "step": "0.01"}),
        }
