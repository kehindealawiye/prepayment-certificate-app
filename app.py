import streamlit as st
import pandas as pd
from io import BytesIO

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background-color: #001f3f;
            color: white;
        }
        html, body, [class*="css"] {
            color: white !important;
            background-color: #001f3f !important;
        }
        label, .stTextInput label, .stSelectbox label, .stNumberInput label, .stRadio label, .stMarkdown, .st-b8, .st-ag, .st-cq, .st-bz {
            color: white !important;
        }
        .stButton>button, .stDownloadButton>button {
            color: white;
            background-color: #004080;
        }
        h1, h2, h3, h4, h5 {
            color: white !important;
        }
        .st-ef, .st-eg, .st-em {
            background-color: #001f3f !important;
            color: white !important;
        }
        .css-1cpxqw2, .css-1cpxqw2:focus {
            background-color: #003366 !important;
            color: white !important;
        }
        .css-1offfwp, .css-1offfwp:focus {
            color: white !important;
        }
        textarea, input {
            color: white !important;
            background-color: #003366 !important;
        }
        div[data-baseweb="select"] {
            background-color: #003366 !important;
            color: white !important;
        }
        div[data-baseweb="select"] * {
            color: white !important;
            background-color: #003366 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Prepayment Certificate Calculator")

# Text Inputs
mda = st.text_input("MDA")
project_title = st.text_input("Project Title")
contractor = st.text_input("Contractor")

# Selection Inputs
payment_stage = st.selectbox("Payment Stage", ["Stage Payment", "Final Payment", "Retention"])
has_retention = st.radio("Is there retention?", ["Yes", "No"])
has_vat = st.radio("Is there VAT?", ["Yes", "No"])

# Percentage Inputs
advance_payment_pct = st.number_input("Percentage of Advance Payment (%)", min_value=0.0, max_value=100.0, step=0.1)
advance_refund_pct = st.number_input("Percentage of Advance Payment Refund (%)", min_value=0.0, max_value=100.0, step=0.1)

# Amount Inputs
total_contract_sum = st.number_input("TOTAL CONTRACT SUM (₦)", min_value=0.0, step=100000.0, format="%.2f")
revised_contract_sum = st.number_input("REVISED CONTRACT SUM (₦)", min_value=0.0, step=100000.0, format="%.2f")
work_completed = st.number_input("WORK COMPLETED TO DATE (₦)", min_value=0.0, step=100000.0, format="%.2f")
previous_payment = st.number_input("PREVIOUS PAYMENT (₦)", min_value=0.0, step=100000.0, format="%.2f")

# Calculate Button
if st.button("Calculate Now"):
    advance_payment = (advance_payment_pct / 100) * total_contract_sum
    retention = 0.05 * work_completed if has_retention == "Yes" else 0
    total_net_payment = work_completed - retention
    vat = 0.075 * total_net_payment if has_vat == "Yes" else 0
    total_net_amount = total_net_payment + vat
    advance_payment_refund = (advance_refund_pct / 100) * advance_payment
    amount_due = total_net_amount - advance_payment_refund - previous_payment

    results = {
        "TOTAL CONTRACT SUM": f"₦{total_contract_sum:,.2f}",
        "REVISED CONTRACT SUM": f"₦{revised_contract_sum:,.2f}",
        "ADVANCE PAYMENT": f"₦{advance_payment:,.2f}",
        "RETENTION": f"₦{retention:,.2f}",
        "TOTAL NET PAYMENT": f"₦{total_net_payment:,.2f}",
        "VAT": f"₦{vat:,.2f}",
        "TOTAL NET AMOUNT": f"₦{total_net_amount:,.2f}",
        "ADVANCE PAYMENT REFUND": f"₦{advance_payment_refund:,.2f}",
        "PREVIOUS PAYMENT": f"₦{previous_payment:,.2f}",
        "AMOUNT DUE": f"₦{amount_due:,.2f}"
    }

    st.subheader("Results")
    for key, val in results.items():
        st.write(f"**{key}:** {val}")

    df_result = pd.DataFrame.from_dict(results, orient='index', columns=["Value"]).reset_index()
    df_result.columns = ["Metric", "Value"]

    # Excel Download Section
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_result.to_excel(writer, index=False, sheet_name='Prepayment Summary')
output.seek(0)

st.download_button(
    label="Download Prepayment Summary as Excel",
    data=output,
    file_name="prepayment_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

)
