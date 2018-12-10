# -*- coding: utf-8 -*-
"""Model de usuários"""

from django.db import models


class PessoaModel(models.Model):
    """"""

    nome = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    disciplina = models.CharField(max_length=1000)
    curso = models.CharField(max_length=1000)
    turma = models.CharField(max_length=1000)

    class Meta:
        app_label = "consultas"

    def __unicode__(self):
        return self.nome
