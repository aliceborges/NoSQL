from django.conf.urls import url
import consultas.views
from consultas.views.views import Pesquisa

app_name = 'consultas'
urlpatterns = [
    url(r'^pesquisar/$', Pesquisa.as_view(), name='pesquisar'),
    url(r'^$', consultas.views.views.index, name='index'),
]
