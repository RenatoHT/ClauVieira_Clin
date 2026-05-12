from django.shortcuts import render, HttpResponse
from .services import PDFgen
from .services import build_pairs
from pathlib import Path
from .forms import CreateFormAnam


def index(request):
    return render(request, "pag_web_clinicas/index.html")


def sobre(request):
    return render(request, "pag_web_clinicas/sobre.html")


def servicos(request):
    return render(request, "pag_web_clinicas/servicos.html")


def contato(request):
    return render(request, "pag_web_clinicas/contato.html")


#####ficha de anamnese######
def form_anam(request):
    personal_fields = ['nome', 'data_nasc', 'rg', 'cpf', 'tel', 'endereco']

    if request.method == "POST":
        form = CreateFormAnam(request.POST)

        if form.is_valid():
            print("IS VALID:", form.is_valid())
            print("ERRORS:", form.errors)
            return gerar_pdf(request, form, form.cleaned_data)
        else:
            print(form.errors)  # DEBUG
    else:
        form = CreateFormAnam()

    fields = build_pairs(form)

    
    context = {
        "form": form,
        "personal_fields": personal_fields,
        "fields": fields
    }

    return render(request, "pag_web_clinicas/form_anam.html", context)

def gerar_pdf(request, form, data):
    BASE_DIR = Path(__file__).resolve().parent

    pdf_service = PDFgen(form, data)
    pdf = pdf_service.generate_pdf()

    file_path = BASE_DIR.parent / 'media' / f"{data['nome']}.pdf"

    #pdf_service.save(file_path, pdf)

    return HttpResponse(pdf, content_type="application/pdf")