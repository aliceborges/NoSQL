from django.shortcuts import render
from django.views import View
from cassandra.cluster import Cluster
from consultas.models import PessoaModel, CursoModel
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from django.views.generic.base import View
from django.shortcuts import render
from neo4jrestclient.client import GraphDatabase,Node
from neo4jrestclient.query import Q
from neo4jrestclient import client
from py2neo import authenticate, Graph, Node, Relationship,Path,Rel
graph = Graph()
from django.http import HttpResponse

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

DB_NAME = 'escola'

authenticate("localhost:7474", "neo4j", "admin")
graph = Graph("http://localhost:7474/db/data/")


def index(request):
    template = "blank.html"
    return render(request, template)


class Pesquisa(View):
    """"""
    template = "mostrar.html"

    def post(self, request):
        """"""
        if request.method == "POST":
            context_dict = {}

            if request.POST.get('pesquisa1') is not None:
                if request.POST.get('pesquisa1') != "":
                    lista = info_usuarios(request.POST.get('pesquisa1'))
                    context_dict = {'Pessoas': lista, 'Nome': True, 'Usuario': True, 'Email': True, 'Senha': True}

            if request.POST.get('pesquisa2') is not None:
                if request.POST.get('pesquisa2') != "":
                    lista = info_curso_duracao_descricao_turmas_by_nome(request.POST.get('pesquisa2'))
                    context_dict = {'Cursos': lista, 'Curso': True, 'Duracao': True, 'Descricao': True, 'Turma': True}

            if request.POST.get('pesquisa3') is not None:
                if request.POST.get('pesquisa3') != "":
                    lista = info_cursos_periodo_by_turma(request.POST.get('pesquisa3'))
                    context_dict = {'Cursos': lista, 'Curso': True, 'Periodo': True}

            if request.POST.get('pesquisa4Curso') is not None:
                if request.POST.get('pesquisa4Curso') != "" and request.POST.get('pesquisa4Turma') != "":
                    lista = info_disciplina_by_curso_and_turma(request.POST.get('pesquisa4Curso'), request.POST.get('pesquisa4Turma'))
                    context_dict = {'Cursos': lista, 'Disciplina': True}

            if request.POST.get('pesquisa5Usuario') is not None:
                if request.POST.get('pesquisa5Usuario') != "" and request.POST.get('pesquisa5Tipo') != "":
                    lista = info_usuarios_disciplinas(request.POST.get('pesquisa5Usuario'), request.POST.get('pesquisa5Tipo'))
                    context_dict = {'Pessoas': lista, 'Disciplina': True}

            if request.POST.get('pesquisa6') is not None:
                if request.POST.get('pesquisa6') != "":
                    lista = info_usuarios_by_tipo(request.POST.get('pesquisa6'))
                    context_dict = {'Pessoas': lista, 'Nome': True, 'Curso': True, 'Disciplina': True, 'Turma': True}

            return render(request, self.template, context_dict)

def info_usuarios(usuario):
    cluster = Cluster()
    session = cluster.connect(DB_NAME)
    session.execute('USE ' + DB_NAME)
    rows = session.execute("select nome, email, usuario, senha  from Pessoa where usuario = '" + usuario + "';");
    pessoas = []

    for query in rows:
        pessoa = PessoaModel()
        pessoa.nome = query.nome
        pessoa.email = query.email
        pessoa.usuario = query.usuario
        pessoa.senha = query.senha
        pessoas.append(pessoa)
    return pessoas


def info_usuarios_disciplinas(nome, tipo):
    cluster = Cluster()
    session = cluster.connect(DB_NAME)
    session.execute('USE ' + DB_NAME)
    rows = session.execute(
        "select disciplina from pessoa where nome = '" + nome + "' and tipo = '" + tipo + "'  ALLOW FILTERING;");
    pessoas = []
    for query in rows:
        pessoa = PessoaModel()
        pessoa.disciplina = query.disciplina
        pessoas.append(pessoa)
        print("----------------------------")
    return pessoas


def info_usuarios_by_tipo(tipo):
    cluster = Cluster()
    session = cluster.connect(DB_NAME)
    session.execute('USE ' + DB_NAME)
    rows = session.execute("select nome, curso, disciplina, turma from pessoa where tipo = '"+tipo+"'  ALLOW FILTERING;")
    pessoas = []
    for query in rows:
        pessoa = PessoaModel()
        pessoa.disciplina = query.disciplina
        pessoa.curso = query.curso
        pessoa.nome = query.nome
        pessoa.turma = query.turma
        pessoas.append(pessoa)
    return pessoas


def info_curso_duracao_descricao_turmas_by_nome(nome_curso):
    cypher = graph.cypher
    results = cypher.execute(
        "MATCH (Curso:" + nome_curso + ")-[:pertence]-(OtherNodes) RETURN  Curso.nomeCurso,Curso.duracao,Curso.descricao,OtherNodes.nomeTURMA")
    cursos = []
    turma = ""

    curso = CursoModel()
    for query in results:
        curso.nome_curso = query[0]
        curso.duracao = query[1]
        curso.descricao = query[2]
        break
    for query in results:
        if query[3] is not None:
            turma += query[3] + " "
    curso.turmas = turma
    cursos.append(curso)
    return cursos


def info_cursos_periodo_by_turma(turma):
    cypher = graph.cypher
    results = cypher.execute("MATCH (a:" + turma + ")-[pertence]->(b)  return a.periodo,b.nomeCurso")
    cursos = []
    for query in results:
        curso = CursoModel()
        curso.periodo = query[0]
        curso.nome_curso = query[1]
        cursos.append(curso)
    return cursos


def info_disciplina_by_curso_and_turma(curso, turma):
    cypher = graph.cypher
    results = cypher.execute(
        "MATCH (n1:" + curso + ")-[:pertence]-(b:" + turma + ")-[:pertence]-(OtherNodes) RETURN  OtherNodes.nomeDisciplina")
    cursos = []
    for query in results:
        if query[0] is not None:
            curso = CursoModel()
            curso.disciplinas = query[0]
            cursos.append(curso)
    return cursos
