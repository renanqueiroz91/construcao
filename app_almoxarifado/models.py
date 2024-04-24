from django.db import models
from django.utils import timezone
class Construcao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Material(models.Model):
    TIPO_CHOICES = [
        ('und', 'Unidade'),
        ('caixa', 'Caixa'),
        ('rolo', 'Rolo'),
        ('par', 'Par'),
        ('kg', 'Quilograma'),
        ('metro', 'Metro'),
        # Adicione mais tipos conforme necessário
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    construcao = models.ForeignKey(Construcao, on_delete=models.CASCADE, null=False)  # Removido o valor padrão

    def __str__(self):
        return f"{self.nome} ({self.tipo}) - {self.construcao}"

class Estoque(models.Model):
    construcao = models.ForeignKey(Construcao, on_delete=models.CASCADE)
    material = models.CharField(max_length=100)  # Alterado para CharField
    tipo_material = models.CharField(max_length=20, default='und')  # Removido o argumento 'choices'
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.material} - {self.construcao} - {self.quantidade} - {self.tipo_material}"




class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    material = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    tipo_movimento = models.CharField(max_length=20, choices=TIPO_MOVIMENTO_CHOICES)
    quantidade = models.PositiveIntegerField(default=0)
    data_movimentacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo_movimento} de {self.material.material.nome} - Quantidade: {self.quantidade} - {self.data_movimentacao}"
