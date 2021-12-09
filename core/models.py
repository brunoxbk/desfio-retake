from django.db import models


class Process(models.Model):
    """
    |> Processo
        |- número do processo
        |- classe
        |- assunto
        |- juiz
    """
    number = models.CharField(verbose_name='número', max_length=120)
    process_class = models.CharField(verbose_name='classe', max_length=120)
    subject = models.CharField(verbose_name='assunto', max_length=120)
    judge = models.CharField(verbose_name='juiz', max_length=120)

    class Meta:
        verbose_name = 'processo'
        verbose_name_plural = 'processos'
        ordering = ('-pk',)

    def __str__(self):
        return self.number


class Part(models.Model):
    """
    |> Partes (Pessoas Vínculadas)
        |- nome
        |- categoria
    """
    process = models.ForeignKey(
        Process, verbose_name="processo",
        on_delete=models.CASCADE,
        related_name='parts')
    name = models.CharField(verbose_name='nome', max_length=120)
    category = models.CharField(verbose_name='categoria', max_length=120)

    class Meta:
        verbose_name = 'parte'
        verbose_name_plural = 'partes'
        ordering = ('-pk',)

    def __str__(self):
        return self.name

