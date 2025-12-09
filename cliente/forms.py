from django import forms
from .models import Cliente , Beneficiario


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format='%Y-%m-%d'
            ),
            "fecha_nacimiento_asegurado": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format='%Y-%m-%d'
            ),
            "fecha_emision": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format='%Y-%m-%d'
            ),
            "fecha_vencimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format='%Y-%m-%d'
            ),

            "poliza": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_contratante": forms.TextInput(attrs={"class": "form-control"}),
            "sobrenombre": forms.TextInput(attrs={"class": "form-control"}),
            "asegurado_principal": forms.TextInput(attrs={"class": "form-control"}),
            "rfc": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "banco": forms.TextInput(attrs={"class": "form-control"}),
            "periodo_pago": forms.Select(attrs={"class": "form-select"}),
            "moneda": forms.Select(attrs={"class": "form-select"}),
            "modo_pago": forms.Select(attrs={"class": "form-select"}),
            "producto": forms.Select(attrs={"class": "form-select"}),
            "estatus_cliente": forms.Select(attrs={"class": "form-select"}),
            "deduce": forms.Select(attrs={"class": "form-select"}),
            "dia_cobro": forms.NumberInput(attrs={"class": "form-control"}),
            "intentos": forms.NumberInput(attrs={"class": "form-control"}),
            "amparado": forms.TextInput(attrs={"class": "form-control"}),
            "rechazo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos de fecha que deben conservar su valor
        date_fields = [
            "fecha_nacimiento",
            "fecha_nacimiento_asegurado",
            "fecha_emision",
            "fecha_vencimiento",
        ]

        for field in date_fields:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field)

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = [
            "nombre_beneficiario",
            "fecha_nacimiento_beneficiario",
            "estatus_beneficiario",
            "parentesco",
        ]

        widgets = {
            "nombre_beneficiario": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "fecha_nacimiento_beneficiario": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "estatus_beneficiario": forms.Select(attrs={
                "class": "form-select"
            }),
            "parentesco": forms.Select(attrs={
                "class": "form-select"
            }),
        }
