from django.shortcuts import render


def index(request):
    return render(request, "pag_web_clinicas/index.html")


def sobre(request):
    return render(request, "pag_web_clinicas/sobre.html")


def servicos(request):
    return render(request, "pag_web_clinicas/servicos.html")


def contato(request):
    return render(request, "pag_web_clinicas/contato.html")
