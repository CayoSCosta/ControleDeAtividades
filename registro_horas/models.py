import uuid
from datetime import datetime, timedelta
from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ativo = models.BooleanField(default=True)
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    data_de_modificacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Define que esta classe será uma base abstrata


class Registro(BaseModel):
    data_de_inicio = models.DateField()
    hora_de_inicio = models.TimeField()
    hora_de_termino = models.TimeField(null=True, blank=True)
    horas_utilizadas = models.FloatField(null=True, blank=True)  # Altera para Float para armazenar horas como número
    hora_de_pausa = models.TimeField(blank=True, null=True)
    tempo_pausado = models.DurationField(default=timedelta(0))  # Acumula tempo de pausas
    ticket = models.CharField(max_length=255, null=True, blank=True)
    cliente = models.CharField(max_length=255, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Registro {self.id} - {self.ticket or 'Sem Ticket'}"

    @property
    def status(self):
        if self.hora_de_pausa:
            return "Pausado"
        elif self.hora_de_termino:
            return "Encerrado"
        else:
            return "Em Andamento"

    def clean(self):
        # Valida se a hora de término é posterior à hora de início
        if self.hora_de_termino and self.hora_de_inicio > self.hora_de_termino:
            raise ValidationError("A hora de término não pode ser anterior à hora de início.")
        super().clean()

    def save(self, *args, **kwargs):
        # Calcula automaticamente as horas utilizadas
        if self.hora_de_inicio and self.hora_de_termino:
            inicio = datetime.combine(self.data_de_inicio, self.hora_de_inicio)
            termino = datetime.combine(self.data_de_inicio, self.hora_de_termino) - self.tempo_pausado
            self.horas_utilizadas = (termino - inicio).total_seconds() / 3600  # Converte segundos em horas
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-data_de_inicio', '-hora_de_inicio']  # Ordena por data e hora de início, mais recentes primeiro
