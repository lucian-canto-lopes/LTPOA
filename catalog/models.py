from django.conf import settings
from django.db import models
from django.urls import reverse


class Sample(models.Model):
    class SampleType(models.TextChoices):
        HONEY = "MEL", "Mel"
        MILK = "LEITE", "Leite"
        OTHER = "OUTRO", "Outro"

    class Status(models.TextChoices):
        RECEIVED = "RECEBIDA", "Recebida"
        ANALYZING = "EM_ANALISE", "Em análise"
        COMPLETED = "CONCLUIDA", "Concluída"
        DISCARDED = "DESCARTADA", "Descartada"

    class Condition(models.TextChoices):
        ADEQUATE = "ADEQUADA", "Adequada"
        INADEQUATE = "INADEQUADA", "Inadequada"
        PENDING = "PENDENTE", "Aguardando avaliação"

    class Unit(models.TextChoices):
        GRAM = "g", "g"
        KILOGRAM = "kg", "kg"
        MILLILITER = "mL", "mL"
        LITER = "L", "L"
        UNIT = "un", "unidade(s)"

    code = models.CharField("código interno", max_length=40, unique=True)
    sample_type = models.CharField("tipo de amostra", max_length=10, choices=SampleType.choices)
    received_at = models.DateField("data de recebimento")
    origin = models.CharField("origem", max_length=180)
    requester = models.CharField("solicitante", max_length=180)
    amount = models.DecimalField("quantidade", max_digits=10, decimal_places=2)
    unit = models.CharField("unidade", max_length=2, choices=Unit.choices)
    condition = models.CharField(
        "condição da amostra",
        max_length=12,
        choices=Condition.choices,
        default=Condition.PENDING,
    )
    status = models.CharField(
        "status",
        max_length=12,
        choices=Status.choices,
        default=Status.RECEIVED,
    )
    notes = models.TextField("observações", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="cadastrada por",
        on_delete=models.PROTECT,
        related_name="samples_created",
    )
    created_at = models.DateTimeField("cadastrada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        ordering = ["-received_at", "-created_at"]
        verbose_name = "amostra"
        verbose_name_plural = "amostras"

    def __str__(self):
        return f"{self.code} — {self.get_sample_type_display()}"

    def get_absolute_url(self):
        return reverse("sample_detail", kwargs={"pk": self.pk})
