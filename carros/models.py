from django.db import models

class Carro(models.Model):
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    ano = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço não pode ser nulo ou vazio
    imagem = models.ImageField(upload_to='carros/', null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    em_estoque = models.BooleanField(default=True)  # Indica se o carro está disponível em estoque
    vendido = models.BooleanField(default=False)  # Marca se o carro foi vendido

    def __str__(self):
        return f"{self.nome} ({self.marca}, {self.ano})"

    def vender_carro(self):
        """Método para marcar o carro como vendido e fora de estoque."""
        if self.vendido:
            raise ValueError(f"O carro {self.nome} já foi vendido.")  # Garantir que o carro não seja vendido novamente
        if self.em_estoque:
            self.em_estoque = False
            self.vendido = True
            self.save()
        else:
            raise ValueError("Carro não disponível para venda, está fora de estoque.")


class Compra(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.SET_NULL, null=True, related_name='compras')
    nome_cliente = models.CharField(max_length=255)
    numero_cliente = models.CharField(max_length=15)
    email_cliente = models.EmailField()
    endereco_cliente = models.CharField(max_length=255)  # Endereço do cliente
    data_compra = models.DateTimeField(auto_now_add=True)  # A data de compra será gerada automaticamente
    confirmado = models.BooleanField(default=True)  # Marca se a compra foi confirmada

    def __str__(self):
        if self.carro:
            return f'{self.nome_cliente} - {self.carro.nome} ({self.data_compra})'
        else:
            return f'{self.nome_cliente} - Carro não disponível ({self.data_compra})'

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para garantir que o carro seja marcado como vendido ao ser comprado."""
        if self.carro:  # Verifica se o carro está associado antes de tentar marcar como vendido
            if not self.carro.vendido:
                self.carro.vendido = True
                self.carro.em_estoque = False
                self.carro.save()
        super().save(*args, **kwargs)
