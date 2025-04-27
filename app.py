import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load the checklist
@st.cache_data
def load_checklist():
    df = pd.read_csv('Checklist.csv')
    return df

df = load_checklist()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'select_department'
if 'selected_department' not in st.session_state:
    st.session_state.selected_department = None

st.title("✅ Department Checklist Form")

# Page 1: Select Department
if st.session_state.page == 'select_department':
    st.subheader("Please select your Department to begin:")

    departments = df['Department'].unique()
    selected_department = st.selectbox("Department", departments)

    if st.button("Start Checklist"):
        st.session_state.selected_department = selected_department
        st.session_state.page = 'checklist'  # Move to checklist page

# Page 2: Checklist
elif st.session_state.page == 'checklist':
    selected_department = st.session_state.selected_department
    st.subheader(f"Checklist for {selected_department}")

    # Filter checklist based on department
    checklist_items = df[df['Department'] == selected_department]

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

    # Option to go back
    if st.button("🔙 Go back to Department Selection"):
        st.session_state.page = 'select_department'
        st.session_state.selected_department = None
