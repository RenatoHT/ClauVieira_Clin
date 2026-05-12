from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils import timezone
from django.utils.formats import date_format

class PDFgen:
    template_name = "pag_web_clinicas/template_pdf.html"

    def __init__(self, form, data: dict):
        self.form = form

        self.data = data

        self.data["fields"] = self.build_pdf_table()
        self.data["path_ass"] = self.assinatura_img(data["assinatura"])

        today = timezone.now()    

        self.data['dia'] = date_format(today, 'd')
        self.data['mes'] = date_format(today, 'F')
        self.data['ano'] = date_format(today, 'Y')

        print(self.data['path_ass'])
    def render_html(self) -> str:
        return render_to_string(self.template_name, self.data)

    def generate_pdf(self) -> bytes:
        html_string = self.render_html()
        return HTML(string=html_string).write_pdf()

    def save(self, path: str, pdf_bytes: bytes):
        with open(path, "wb") as f:
            f.write(pdf_bytes)

    def assinatura_img(self, c_form):
        from pathlib import Path
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        data = c_form

        plt.figure()

        for shape in data:
            plt.plot(shape["x"], shape["y"], color="black")

        plt.gca().invert_yaxis()   # optional: image-like coordinates
        plt.axis("equal")
        plt.axis("off")


        output_dir = Path("media")
        output_dir.mkdir(parents=True, exist_ok=True)

        base_dir = Path(__file__).resolve().parent
        file_path = base_dir.parent / output_dir / "assinatura.png"

        plt.savefig(file_path, dpi=300, bbox_inches="tight", pad_inches=0, transparent = True)
        plt.close()
        
        return str(file_path)
    
    #tabela pdf
    def build_pdf_table(self):
        rows = []

        for key in self.data:
            if key.endswith("_bool"):
                base = key[:-5]

                bool_field = self.form[base + "_bool"]
                str_field = self.form[base + "_str"]

                rows.append({
                    "label": bool_field.label,     # ✔ real label
                    "bool": self.data[key],
                    "text": self.data.get(base + "_str", "") if self.data[key] else ""
                })

        return rows


#para criação do forms em view
def build_pairs(form):
    pairs = []

    for name in form.fields:
        if name.endswith("_bool"):
            base = name[:-5]
            str_name = base + "_str"

            if str_name in form.fields:
                pairs.append((
                    form[name],
                    form[str_name]
                ))

    return pairs
