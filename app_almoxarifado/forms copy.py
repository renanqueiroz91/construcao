from django import forms
from .models import Estoque, Material, Construcao

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['construcao', 'material', 'tipo_material', 'quantidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.all()

        # Removi a adição do campo tipo ao formulário, pois agora ele é parte do modelo

class ConstrucaoForm(forms.ModelForm):
    class Meta:
        model = Construcao
        fields = ['nome']