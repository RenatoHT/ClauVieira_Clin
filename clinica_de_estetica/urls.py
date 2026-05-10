from django.contrib import admin
from django.urls import path, include
from pag_web_clinicas import views

# Rota - biomedica_esteta_clauvieira.com.br
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("servicos/", views.servicos, name="servicos"),
    path("contato/", views.contato, name="contato"),
]
