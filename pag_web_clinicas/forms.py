from django import forms
from jsignature.widgets import JSignatureWidget
from jsignature.forms import JSignatureField
from .models import Cadastro
import re
from datetime import date

#variáveis e função auxiliar para padronização dos nomes
NOME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[ '\-][A-Za-zÀ-ÖØ-öø-ÿ]+)*$")

MINUSCULAS = {'da', 'de', 'do', 'das', 'dos', 'e', 'van', 'von', 'del', 'di', 'du'}


def formatar_nome(nome: str) -> str:

    partes = nome.strip().split()
    resultado = []

    for i, p in enumerate(partes):
        p_lower = p.lower()

        if i > 0 and p_lower in MINUSCULAS:
            resultado.append(p_lower)
        else:
            resultado.append(p.capitalize())

    return " ".join(resultado)

#formulário
class CreateFormAnam(forms.ModelForm):

    #esconde endereço completo
    endereco = forms.CharField(required=False)

    #widgets data_nascimento e assinatura
    data_nasc = forms.DateField(label="Data de Nascimento",
                            input_formats=['%d/%m/%Y'],
                            widget=forms.DateInput(
                                format='%d/%m/%Y',
                                attrs={'placeholder': 'dd/mm/aaaa',
                                    }
                                )
                            )
    infoadd = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'id_infoadd',
            'rows': 6,
        })
    )

    assinatura = JSignatureField(label="Assinatura",
                                 widget=JSignatureWidget(
                                                        jsignature_attrs={
                                                                        'color': "#000000", 
                                                                        'height': '200px', 
                                                                        'width': '100%', 
                                                                        "ResetButton":True}))
    

    class Meta:
        model = Cadastro
        fields = '__all__'
        exclude = ["endereco"]

        labels = {
            'nome': 'Nome Completo',
            'rg': 'R.G',
            'cpf': 'CPF',
            'tel': "Telefone",
            'assinatura': 'Assinatura',
            'endereco': 'Endereço',
            'uf': 'UF',
            'numero': 'Número',
            'alergia_bool': 'Alergias',
            'alergia_str':'',
            'hepatite_bool': 'Hepatite',
            'hepatite_str':'',
            'hiv_bool': 'HIV',
            'hiv_str':'',
            'gravida_bool': 'Grávida',
            'gravida_str':'',
            'amamentando_bool': 'Amamentando',
            'amamentando_str':'',
            'diabetes_bool': 'Diabetes',
            'diabetes_str':'',
            'hipertensao_bool': 'Hipertensão',
            'hipertensao_str':'',
            'probcard_bool': 'Problemas Cardíacos',
            'probcard_str':'',
            'probresp_bool': 'Problemas Respiratórios',
            'probresp_str':'',
            'depre_bool': 'Depressão',
            'depre_str':'',
            'acne_bool': 'Possui acne ativa?',
            'acne_str':'',
            'trombvari_bool': 'Faz tratamento de trombose e varizez?',
            'trombvari_str':'',
            'herpes_bool': 'Herpes Labial',
            'herpes_str':'',
            'ilicita_bool': 'Faz uso de substâncias ilícitas?',
            'ilicita_str':'',
            'medicamento_bool': 'Faz uso de algum medicamento?',
            'medicamento_str':'',
            'dente_bool': 'Está em tratamento dentário?',
            'dente_str':'',
            'injeta_bool': 'Algum produto injetável na face?',
            'injeta_str':'',
            'proce_bool': 'Procedimentos faciais nos últimos 30 dias?',
            'proce_str':'',
            'plastica_bool': 'Cirurgia plástica recente?',
            'plastica_str':'',
            'doenca_bool': 'Doença crônica ou autoimune?',
            'doenca_str':'',
            'infoadd':'Existe alguma informação que julgue necessário informar ao profissional?',
            
        }

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Digite o nome completo",
                "maxlength": 200,
            }),
            'rg': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Somente Números",
                "maxlength": 9,
            }),
            'cpf': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Somente Números",
                "maxlength": 11,
            }),
            'tel': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "DDD + Números",
                "maxlength": 11,
            }),
            "herpes_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Última occorrência?"
            }),
            "ilicita_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
            "medicamento_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
            "dente_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
            "proce_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
            "plastica_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
            "ilicita_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
            "doenca_str": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Qual?"
            }),
        }
    

    #validadore nome
    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()

        if len(nome) < 2:
            raise forms.ValidationError("Nome muito curto.")

        if not NOME_REGEX.fullmatch(nome):
            raise forms.ValidationError("Nome inválido.")

        return formatar_nome(nome)
    
    #validador data nascimento
    def clean_data_nasc(self):
        nascimento = self.cleaned_data["data_nasc"]
        hoje = date.today()

        if nascimento > hoje:
            raise forms.ValidationError("Data de nascimento não pode ser no futuro.")

        if nascimento.year < 1900:
            raise forms.ValidationError("Data de nascimento inválida.")

        idade = hoje.year - nascimento.year - (
            (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
        )

        if idade > 120:
            raise forms.ValidationError("Idade inválida.")

        return nascimento

    #validador cpf
    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]

        # keep only digits
        cpf = ''.join(filter(str.isdigit, str(cpf)))

        # length check
        if len(cpf) != 11:
            raise forms.ValidationError("CPF inválido.")

        # reject repeated digits
        if cpf == cpf[0] * 11:
            raise forms.ValidationError("CPF inválido.")

        # validate digits
        for pos in (9, 10):
            soma = sum(int(cpf[i]) * ((pos + 1) - i) for i in range(pos))
            resto = soma % 11
            digito = 0 if resto < 2 else 11 - resto

            if int(cpf[pos]) != digito:
                raise forms.ValidationError("CPF inválido.")

        # return formatted CPF
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')

        tel = ''.join(filter(str.isdigit, str(tel)))

        # Verifica se o telefone é fixo ou celular
        if len(tel) not in (10, 11):
            raise forms.ValidationError(
                'Telefone deve possuir 10 ou 11 dígitos.'
            )

        # Valida DDD
        ddd = int(tel[:2])

        if not (11 <= ddd <= 99):
            raise forms.ValidationError('DDD inválido.')

        # Evita números repetidos
        if tel == tel[0] * len(tel):
            raise forms.ValidationError('Telefone inválido.')

        # Celular deve começar com 9
        if len(tel) == 11 and tel[2] != '9':
            raise forms.ValidationError('Celular inválido.')

        # Fixo não pode começar com 9
        if len(tel) == 10 and tel[2] == '9':
            raise forms.ValidationError('Telefone fixo inválido.')

        # Formata antes de salvar
        if len(tel) == 11:
            return f'({tel[:2]}) {tel[2:7]}-{tel[7:]}'

        return f'({tel[:2]}) {tel[2:6]}-{tel[6:]}'
    
    def clean_rg(self):
        value = self.cleaned_data["rg"]

        if not isinstance(value, (str, int)):
            raise forms.ValidationError("RG deve ser texto ou número")
    
        v = str(value).strip()
        rg_limpo = re.sub(r"[.\-\s]", "", v)

        if not (rg_limpo.isdigit() or (rg_limpo[:-1].isdigit() and rg_limpo[-1].upper() == "X")):
            raise forms.ValidationError("RG deve conter apenas números, pontos ou hífens")
        
        if len(rg_limpo) < 7 or len(rg_limpo) > 9:
            raise forms.ValidationError("RG deve ter entre 7 e 9 dígitos")
        
        # Validação: todos os dígitos iguais é inválido
        if len(set(rg_limpo)) == 1: raise ValueError("RG inválido: todos os dígitos são iguais")

        if len(rg_limpo) == 7:
            return f"{rg_limpo[:2]}.{rg_limpo[2:5]}.{rg_limpo[5:]}"
        elif len(rg_limpo) == 8:
            return f"{rg_limpo[:3]}.{rg_limpo[3:6]}.{rg_limpo[6:]}"
        else:  # 9 digits
            return f"{rg_limpo[:2]}.{rg_limpo[2:5]}.{rg_limpo[5:8]}-{rg_limpo[8]}"
        
    def clean_cep(self):
        cep = self.cleaned_data["cep"]
        cep = re.sub(r"\D", "", str(cep))

        if len(cep) != 8:
            raise forms.ValidationError("CEP deve conter 8 dígitos")

        return cep

    def clean(self):
        cleaned = super().clean()

        partes = []

        if cleaned.get("logradouro"):
            partes.append(cleaned["logradouro"])

        if cleaned.get("numero"):
            partes.append(cleaned["numero"])

        if cleaned.get("bairro"):
            partes.append(cleaned["bairro"])

        if cleaned.get("cidade"):
            partes.append(cleaned["cidade"])

        if cleaned.get("uf"):
            partes.append(cleaned["uf"])

        if cleaned.get("cep"):
            partes.append(f"CEP: {cleaned['cep']}")

        partes = [p.strip().title() for p in partes if p]

        cleaned["endereco"] = (", ".join(partes[:-1])) + ' - ' + partes[-1].upper()

        print("CLEANED DATA BEFORE:", cleaned)

        return cleaned