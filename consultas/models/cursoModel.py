# -*- coding: utf-8 -*-
"""Model de usuários"""

from django.db import models


class CursoModel(models.Model):
    """"""

    nome_curso = models.CharField(max_length=255)
    duracao = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    periodo = models.CharField(max_length=255)
    turmas = models.CharField(max_length=1000)
    disciplinas = models.CharField(max_length=1000)

    class Meta:
        app_label = "consultas"

    def __unicode__(self):
        return self.nome_curso
