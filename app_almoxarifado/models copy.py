from django.db import models

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


