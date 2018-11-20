from django.shortcuts import render
from django.views import View
from pirates import models
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from pirates import forms
from django.shortcuts import redirect


class ListaTesourosView(View):
    def get(self, request):
        lista_tesouros = models.Tesouro.objects.annotate(
            total=ExpressionWrapper(
                F('preco') * F('quantidade'),
                output_field=DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    blank=True
                )
            )
        ).all()
        return render(
            request,
            template_name='lista_tesouros.html',
            context=dict(
                lista_tesouros=lista_tesouros,
                total_geral=lista_tesouros.aggregate(Sum('total'))['total__sum']
            )
        )


class SalvarTesouroView(View):
    def get(self, request, pk=None):
        if pk:
            form = forms.TesouroForm(
                instance=models.Tesouro.objects.get(pk=pk)
            )
        else:
            form = forms.TesouroForm
        if pk:
            return render(
                request,
                template_name='salvar_tesouro.html',
                context=dict(
                    form=form,
                    action='/edit/{}'.format(pk)
                )
            )

        else:
            return render(
                request,
                template_name='salvar_tesouro.html',
                context=dict(
                    form=form,
                    action='new'
                )
            )

    def post(self, request, pk=None):
        form = forms.TesouroForm(request.POST, request.FILES, instance=models.Tesouro.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return redirect('list')

        if pk:
            return render(
                request,
                template_name='salvar_tesouro.html',
                context=dict(
                    form=form,
                    action='/edit/{}'.format(pk)
                )
            )

        else:
            return render(
                request,
                template_name='salvar_tesouro.html',
                context=dict(
                    form=form,
                    action='new'
                )
            )


class DeletarTesouroView(View):
    def get(self, request, pk=None):
        models.Tesouro.objects.get(pk=pk).delete()
        return redirect('list')
