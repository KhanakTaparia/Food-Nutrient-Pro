from fpdf import FPDF
from datetime import date

def generate_pdf(user, totals, df, filename="nutrition_report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Nutrition Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"User: {user}", ln=True)
    pdf.cell(200, 10, f"Date: {date.today()}", ln=True)

    pdf.ln(10)

    # Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Daily Summary", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Calories: {round(totals['calories'],2)}", ln=True)
    pdf.cell(200, 10, f"Protein: {round(totals['protein'],2)} g", ln=True)
    pdf.cell(200, 10, f"Carbs: {round(totals['carbs'],2)} g", ln=True)
    pdf.cell(200, 10, f"Fat: {round(totals['fat'],2)} g", ln=True)

    pdf.ln(10)

    # Meal log
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Meals", ln=True)

    pdf.set_font("Arial", "", 10)

    for _, row in df.iterrows():
        line = f"{row['food']} | {row['grams']}g | C:{row['calories']:.1f}"
        pdf.cell(200, 8, line, ln=True)

    pdf.output(filename)
    return filename