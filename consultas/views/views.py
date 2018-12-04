from django.shortcuts import render
from django.views import View
from cassandra.cluster import Cluster
from consultas.models import PessoaModel

DB_NAME = 'escola'


def index(request):
    template = "blank.html"
    return render(request, template)


class Pesquisa(View):
    """"""
    template = "mostrar.html"

    def post(self, request):
        """"""
        if request.method == "POST":
            if request.POST.get('pesquisa1') is not None:
                lista = info_usuarios(request.POST.get('pesquisa1'))
            if request.POST.get('pesquisa2') is not None:
                lista = info_usuarios(request.POST.get('pesquisa2'))
            if request.POST.get('pesquisa3') is not None:
                lista = info_usuarios(request.POST.get('pesquisa3'))
            if request.POST.get('pesquisa4Curso') is not None:
                lista = info_usuarios_disciplinas(request.POST.get('pesquisa4Curso'), request.POST.get('pesquisa4Turma'))
            if request.POST.get('pesquisa5Usuario') is not None:
                lista = info_usuarios_disciplinas(request.POST.get('pesquisa5Usuario'),request.POST.get('pesquisa5Tipo'))
            if request.POST.get('pesquisa6') is not None:
                lista =info_usuarios_by_tipo(request.POST.get('pesquisa6'))
            context_dict = {'Pessoas': lista}
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
        print(pessoa.nome, pessoa.usuario, pessoa.senha, pessoa.email)
        print("----------------------------")
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
        print (pessoa.disciplina)
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


