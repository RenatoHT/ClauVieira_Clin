from django.contrib import admin
from .models import (
    Evolucao,
    PlanoAplicacao,
    Profissional,
    Cliente,
    Procedimento,
    TermoConsentimento,
    FichaAnamnese,
    RespostaAnamnese,
)

admin.site.register(Evolucao)
admin.site.register(PlanoAplicacao)
admin.site.register(Profissional)
admin.site.register(Cliente)
admin.site.register(Procedimento)
admin.site.register(TermoConsentimento)
admin.site.register(FichaAnamnese)
admin.site.register(RespostaAnamnese)
