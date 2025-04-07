import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Prepayment Certificate Calculator Cross-Check")

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
    # Computations
    advance_payment = (advance_payment_pct / 100) * total_contract_sum
    retention = 0.05 * work_completed if has_retention == "Yes" else 0
    total_net_payment = work_completed - retention
    vat = 0.075 * total_net_payment if has_vat == "Yes" else 0
    total_net_amount = total_net_payment + vat
    advance_payment_refund = (advance_refund_pct / 100) * advance_payment
    amount_due = total_net_amount - advance_payment_refund - previous_payment

    # Results dictionary
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

    # Display Results
    st.subheader("Results")
    for key, val in results.items():
        st.write(f"**{key}:** {val}")

    # Prepare for download
    df_result = pd.DataFrame.from_dict(results, orient='index', columns=["Value"]).reset_index()
    df_result.columns = ["Metric", "Value"]

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_result.to_excel(writer, index=False, sheet_name='Prepayment Summary')
    output.seek(0)
    st.download_button("Download Excel", data=output.read(), file_name="prepayment_certificate.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
