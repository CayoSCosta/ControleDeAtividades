from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = [
            'ticket', 
            'descricao', 
            'cliente',
            # 'data_de_inicio',
            # 'hora_de_inicio',
            # 'hora_de_termino',
            # 'horas_utilizadas',
        ]
        widgets = {
            'ticket': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o número do ticket',
                }
            ),
            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Digite a descrição do ticket',
                }
            ),
            'cliente': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o nome do cliente',
                }
            ),
            # 'data_de_inicio': forms.DateInput(
            #     attrs={
            #         'type': 'date',
            #         'class': 'form-control',
            #     }
            # ),
            # 'hora_de_inicio': forms.TimeInput(
            #     attrs={
            #         'type': 'time',
            #         'class': 'form-control',
            #     }
            # ),
            # 'hora_de_termino': forms.TimeInput(
            #     attrs={
            #         'type': 'time',
            #         'class': 'form-control',
            #     }
            # ),
            # 'horas_utilizadas': forms.TimeInput(
            #     attrs={
            #         'type': 'time',
            #         'class': 'form-control',
            #         'readonly': 'readonly',  # Campo apenas leitura, calculado automaticamente
            #     }
            # ),
        }
