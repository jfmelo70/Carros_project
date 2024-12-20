from django import forms
from .models import Carro, Compra

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ['nome', 'marca', 'ano', 'preco', 'imagem', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do carro'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a marca do carro'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ano de fabricação'
            }),
            'preco': forms.NumberInput(attrs={  # Usar NumberInput para valores numéricos
                'class': 'form-control',
                'placeholder': 'Digite o preço (R$)',
                'type': 'number',
                'step': '0.01'  # Permite valores decimais
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite uma descrição para o carro',
                'rows': 4
            }),
        }

    # Limpeza de campos
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco and preco < 0:
            raise forms.ValidationError("O preço não pode ser negativo.")
        return preco

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        if not imagem:
            raise forms.ValidationError("Por favor, selecione uma imagem para o carro.")
        return imagem


# Formulário para realizar a compra
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['nome_cliente', 'numero_cliente', 'email_cliente', 'endereco_cliente', 'carro']  # Alterado 'cidade_cliente' para 'endereco_cliente'
        widgets = {
            'nome_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo'
            }),
            'numero_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu número de telefone'
            }),
            'email_cliente': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu e-mail'
            }),
            'endereco_cliente': forms.TextInput(attrs={  # Alterado para 'endereco_cliente'
                'class': 'form-control',
                'placeholder': 'Digite seu endereço completo'
            }),
            'carro': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Escolha um carro'
            }),
        }

    # Verifica se o carro está disponível para a compra
    def clean(self):
        cleaned_data = super().clean()
        carro = self.cleaned_data.get('carro')
        if carro and not carro.em_estoque:
            raise forms.ValidationError("Este carro não está mais disponível para venda.")
        return cleaned_data


# Formulário para o contato
class ContatoForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        }),
        label="Nome"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        }),
        label="E-mail"
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua mensagem',
            'rows': 4
        }),
        label="Mensagem"
    )
