from reportlab.pdfgen import canvas

def generate_pdf(review):

    filename = "review_report.pdf"

    pdf = canvas.Canvas(filename)

    pdf.drawString(
        50,
        800,
        "AI Code Review Report"
    )

    y = 760

    for line in review.split("\n"):

        pdf.drawString(
            50,
            y,
            line[:100]
        )

        y -= 20

        if y <= 50:
            pdf.showPage()
            y = 800

    pdf.save()

    return filename