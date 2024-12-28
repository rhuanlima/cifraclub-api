from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import requests


def create_pdf_with_columns_portrait(data_list, output_pdf):
    # Configurações básicas para o formato retrato
    page_width, page_height = A4
    margin = 0.2 * inch
    column_gap = 0.1 * inch
    column_width = (page_width - 2 * margin - column_gap) / 2

    # Iniciar canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)

    for data in data_list:
        text_obj = c.beginText()
        text_obj.setFont("Courier", 9)
        text_obj.setTextOrigin(margin, page_height - margin)

        title = data["title"]
        link = data["link"]

        # Extrair artista e música do link
        artista, musica = link.rstrip("/").split("/")[-2:]
        url = f"http://localhost:3000/artists/{artista}/songs/{musica}"
        response = requests.get(url)
        response.raise_for_status()
        text = response.text

        # Escrever título (opcional)
        text_obj.setFont("Courier-Bold", 10)
        text_obj.textLine(f"{title}")
        text_obj.setFont("Courier", 9)
        text_obj.textLine("")  # Linha em branco

        column = 0
        for line in text.splitlines():
            if text_obj.getY() < margin:
                # Alternar coluna ou adicionar nova página
                if column == 0:
                    column = 1
                    text_obj.setTextOrigin(
                        margin + column_width + column_gap, page_height - margin
                    )
                else:
                    c.drawText(text_obj)
                    c.showPage()
                    text_obj = c.beginText()
                    text_obj.setFont("Courier", 9)
                    text_obj.setTextOrigin(margin, page_height - margin)
                    column = 0

            # Adicionar linha ao texto
            text_obj.textLine(line.rstrip())

        # Renderizar o conteúdo do link na página atual
        c.drawText(text_obj)
        c.showPage()  # Garantir nova página para o próximo link

    # Renderizar a última página
    c.save()
