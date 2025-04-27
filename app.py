import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load the checklist
@st.cache_data
def load_checklist():
    df = pd.read_csv('Checklist.csv')
    return df

df = load_checklist()

st.title("✅ Department Checklist Form")

# Sidebar for department selection
departments = df['Department'].unique()
selected_department = st.sidebar.selectbox("Select Your Department", departments)

# Filter checklist based on department
checklist_items = df[df['Department'] == selected_department]

st.subheader(f"Checklist for {selected_department}")

# Initialize answers dictionary
answers = {}

# Display checklist items with YES/NO radio buttons
for idx, row in checklist_items.iterrows():
    answer = st.radio(f"{row['Checklist']}", ["YES", "NO"], key=idx)
    answers[row['Checklist']] = answer

# Function to create PDF
def create_pdf(department, answers):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Checklist Report - {department}", ln=True, align='C')
    pdf.ln(10)

    for item, answer in answers.items():
        pdf.multi_cell(0, 10, f"✔️ {item}\nAnswer: {answer}")
        pdf.ln(2)

    pdf_path = "Checklist_Report.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Button to generate PDF
if st.button("Generate PDF Report"):
    pdf_file = create_pdf(selected_department, answers)
    
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="Checklist_Report.pdf")
