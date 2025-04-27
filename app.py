import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load the checklist
@st.cache_data
def load_checklist():
    df = pd.read_csv('Checklist.csv')
    return df

df = load_checklist()

# Inject CSS to make radio button labels bigger
st.markdown(
    """
    <style>
    div.row-widget.stRadio > div{flex-direction:row;}
    label[data-baseweb="radio"] > div:first-child {
        transform: scale(1.5);
    }
    label[data-baseweb="radio"] > div:last-child {
        font-size: 22px;
        padding-left: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

    with st.form("department_form"):
        selected_department = st.selectbox("Department", departments)
        start = st.form_submit_button("Start Checklist")
        
        if start:
            st.session_state.selected_department = selected_department
            st.session_state.page = 'checklist'

# Page 2: Checklist
if st.session_state.page == 'checklist':
    selected_department = st.session_state.selected_department
    st.subheader(f"Checklist for {selected_department}")

    checklist_items = df[df['Department'] == selected_department]

    answers = {}

    for idx, row in checklist_items.iterrows():
        cols = st.columns([5, 2])
        with cols[0]:
            st.write(f"**{idx+1}. {row['Checklist']}**")
        with cols[1]:
            yes_no = st.radio("", ["YES", "NO"], key=f"answer_{idx}", horizontal=True)
            answers[row['Checklist']] = yes_no

    # Function to create PDF in table format
    def create_pdf(department, answers):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)

        # Title
        pdf.cell(0, 10, f"Checklist Report - {department}", ln=True, align='C')
        pdf.ln(10)

        # Table header
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(130, 10, "Checklist Item", border=1, align='C')
        pdf.cell(30, 10, "YES", border=1, align='C')
        pdf.cell(30, 10, "NO", border=1, align='C')
        pdf.ln()

        # Table body
        pdf.set_font('DejaVu', '', 12)
        for item, answer in answers.items():
            pdf.cell(130, 10, item, border=1)
            if answer == "YES":
                pdf.cell(30, 10, "✔️", border=1, align='C')
                pdf.cell(30, 10, "", border=1)
            else:
                pdf.cell(30, 10, "", border=1)
                pdf.cell(30, 10, "✔️", border=1, align='C')
            pdf.ln()

        pdf_path = "Checklist_Report.pdf"
        pdf.output(pdf_path)
        return pdf_path

    if st.button("Generate PDF Report"):
        try:
            pdf_file = create_pdf(selected_department, answers)
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, file_name="Checklist_Report.pdf")
        except Exception as e:
            st.error(f"PDF Generation Error: {e}")

    if st.button("🔙 Go back to Department Selection"):
        st.session_state.page = 'select_department'
        st.session_state.selected_department = None
