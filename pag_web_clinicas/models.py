from django.db import models


# CLIENTE
class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=False, blank=False)
    data_nascimento = models.DateField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, null=False, blank=False)
    endereco = models.CharField(max_length=300)
    email = models.EmailField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cliente"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


# PROFISSIONAL
class Profissional(models.Model):
    nome = models.CharField(max_length=200)
    especialidade = models.CharField(max_length=100)

    registro_conselho = models.CharField(max_length=50, unique=True)

    conselho = models.CharField(max_length=20)

    telefone = models.CharField(max_length=20, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profissional"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"


# PROCEDIMENTO
class Procedimento(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    descricao = models.TextField(blank=True, null=True)

    duracao_media = models.IntegerField(
        blank=True, null=True, help_text="Duração média em minutos"
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "procedimento"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


# TERMO DE CONSENTIMENTO
class TermoConsentimento(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.RESTRICT, related_name="termos"
    )

    profissional = models.ForeignKey(
        Profissional, on_delete=models.RESTRICT, related_name="termos"
    )

    procedimento = models.ForeignKey(
        Procedimento, on_delete=models.RESTRICT, related_name="termos"
    )

    texto_termo = models.TextField()

    local_assinatura = models.CharField(max_length=100)

    data_assinatura = models.DateField()

    assinatura_digital = models.BinaryField(blank=True, null=True)

    consentimento_aceito = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "termo_consentimento"

    def __str__(self):
        return f"Termo - {self.cliente.nome}"


# PERGUNTA ANAMNESE
class PerguntaAnamnese(models.Model):

    class TipoResposta(models.TextChoices):
        SIM_NAO = "SIM_NAO", "Sim/Não"
        TEXTO = "TEXTO", "Texto"
        DATA = "DATA", "Data"
        SIM_NAO_QUAL = "SIM_NAO_QUAL", "Sim/Não + Qual"

    procedimento = models.ForeignKey(
        Procedimento,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="perguntas",
    )

    texto_pergunta = models.CharField(max_length=300)

    tipo_resposta = models.CharField(
        max_length=20, choices=TipoResposta.choices, default=TipoResposta.SIM_NAO
    )

    possui_complemento = models.BooleanField(default=False)

    label_complemento = models.CharField(max_length=100, blank=True, null=True)

    ordem = models.IntegerField(default=0)

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pergunta_anamnese"
        ordering = ["ordem"]

    def __str__(self):
        return self.texto_pergunta


# FICHA ANAMNESE
class FichaAnamnese(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "RASCUNHO", "Rascunho"
        CONCLUIDO = "CONCLUIDO", "Concluído"

    cliente = models.ForeignKey(
        Cliente, on_delete=models.RESTRICT, related_name="fichas_anamnese"
    )

    profissional = models.ForeignKey(
        Profissional, on_delete=models.RESTRICT, related_name="fichas_anamnese"
    )

    procedimento = models.ForeignKey(
        Procedimento, on_delete=models.RESTRICT, related_name="fichas_anamnese"
    )

    local_assinatura = models.CharField(max_length=100, blank=True, null=True)

    data_preenchimento = models.DateField()

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.RASCUNHO
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ficha_anamnese"

    def __str__(self):
        return f"Ficha - {self.cliente.nome}"


# RESPOSTA ANAMNESE
class RespostaAnamnese(models.Model):
    ficha_anamnese = models.ForeignKey(
        FichaAnamnese, on_delete=models.CASCADE, related_name="respostas"
    )

    pergunta = models.ForeignKey(
        PerguntaAnamnese, on_delete=models.RESTRICT, related_name="respostas"
    )

    resposta_sim_nao = models.BooleanField(blank=True, null=True)

    complemento = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resposta_anamnese"

        constraints = [
            models.UniqueConstraint(
                fields=["ficha_anamnese", "pergunta"], name="uq_ficha_pergunta"
            )
        ]

    def __str__(self):
        return f"{self.ficha_anamnese} - {self.pergunta}"


# PLANO APLICACAO
class PlanoAplicacao(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.RESTRICT, related_name="planos"
    )

    profissional = models.ForeignKey(
        Profissional, on_delete=models.RESTRICT, related_name="planos"
    )

    procedimento = models.ForeignKey(
        Procedimento, on_delete=models.RESTRICT, related_name="planos"
    )

    termo = models.ForeignKey(
        TermoConsentimento,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="planos",
    )

    ficha_anamnese = models.ForeignKey(
        FichaAnamnese,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="planos",
    )

    data_aplicacao = models.DateField()

    observacoes = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plano_aplicacao"

    def __str__(self):
        return f"Plano - {self.cliente.nome}"


# EVOLUCAO
class Evolucao(models.Model):
    plano_aplicacao = models.ForeignKey(
        PlanoAplicacao, on_delete=models.CASCADE, related_name="evolucoes"
    )

    profissional = models.ForeignKey(
        Profissional, on_delete=models.RESTRICT, related_name="evolucoes"
    )

    data_registro = models.DateField()

    descricao = models.TextField()

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "evolucao"
        ordering = ["-data_registro"]

    def __str__(self):
        return f"Evolução - {self.plano_aplicacao}"
