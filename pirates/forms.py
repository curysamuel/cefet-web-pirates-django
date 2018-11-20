from django.forms import ModelForm
from . import models

class TesouroForm(ModelForm):
    class Meta:
        model = models.Tesouro
        fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
