import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Prepayment Certificate Calculator", layout="centered")

st.title("Prepayment Certificate Calculator")

# Input Fields
mda = st.text_input("MDA")
project_title = st.text_input("Project Title")
contractor = st.text_input("Contractor")
payment_stage = st.selectbox("Payment Stage", ["Stage Payment", "Final Payment", "Retention"])
has_retention = st.radio("Is there retention?", ["Yes", "No"]) == "Yes"
has_vat = st.radio("Is there VAT?", ["Yes", "No"]) == "Yes"
advance_payment_percent = st.number_input("Advance Payment (%)", min_value=0.0, max_value=100.0, format="%.2f")
advance_payment_refund_percent = st.number_input("Advance Payment Refund (%)", min_value=0.0, max_value=100.0, format="%.2f")

st.markdown("---")
total_contract_sum = st.number_input("Total Contract Sum (₦)", min_value=0.0, format="%.2f")
revised_contract_sum = st.number_input("Revised Contract Sum (₦)", min_value=0.0, format="%.2f")
advance_payment = (advance_payment_percent / 100) * total_contract_sum

work_completed_to_date = st.number_input("Work Completed to Date (₦)", min_value=0.0, format="%.2f")
retention = 0.05 * work_completed_to_date if has_retention else 0.0
total_net_payment = work_completed_to_date - retention
vat = 0.075 * total_net_payment if has_vat else 0.0
total_net_amount = total_net_payment + vat
advance_payment_refund = (advance_payment_refund_percent / 100) * advance_payment
previous_payment = st.number_input("Previous Payment (₦)", min_value=0.0, format="%.2f")
amount_due = total_net_amount - advance_payment_refund - previous_payment

# Display Results
st.subheader("Result")

st.markdown(f"**Total Contract Sum:** ₦{total_contract_sum:,.2f}")
st.markdown(f"**Revised Contract Sum:** ₦{revised_contract_sum:,.2f}")
st.markdown(f"**Advance Payment ({advance_payment_percent}%):** ₦{advance_payment:,.2f}")
st.markdown(f"**Work Completed to Date:** ₦{work_completed_to_date:,.2f}")

if has_retention:
    st.markdown(f"**Retention (5%):** ₦{retention:,.2f}")
else:
    st.markdown("**Retention:** Not Applicable")

st.markdown(f"**Total Net Payment (less retention):** ₦{total_net_payment:,.2f}")

if has_vat:
    st.markdown(f"**VAT (7.5%):** ₦{vat:,.2f}")
else:
    st.markdown("**VAT:** Not Applicable")

st.markdown(f"**Total Net Amount (incl. VAT):** ₦{total_net_amount:,.2f}")
st.markdown(f"**Advance Payment Refund ({advance_payment_refund_percent}%):** ₦{advance_payment_refund:,.2f}")
st.markdown(f"**Previous Payment:** ₦{previous_payment:,.2f}")
st.markdown(f"**Amount Due:** ₦{amount_due:,.2f}")

# Excel Download
data = {
    "Total Contract Sum": [f"₦{total_contract_sum:,.2f}"],
    "Revised Contract Sum": [f"₦{revised_contract_sum:,.2f}"],
    "Advance Payment": [f"₦{advance_payment:,.2f}"],
    "Work Completed to Date": [f"₦{work_completed_to_date:,.2f}"],
    "Retention": [f"₦{retention:,.2f}" if has_retention else "N/A"],
    "Total Net Payment": [f"₦{total_net_payment:,.2f}"],
    "VAT": [f"₦{vat:,.2f}" if has_vat else "N/A"],
    "Total Net Amount": [f"₦{total_net_amount:,.2f}"],
    "Advance Payment Refund": [f"₦{advance_payment_refund:,.2f}"],
    "Previous Payment": [f"₦{previous_payment:,.2f}"],
    "Amount Due": [f"₦{amount_due:,.2f}"]
}
df_result = pd.DataFrame(data)

output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_result.to_excel(writer, index=False, sheet_name='Prepayment Summary')
    writer.save()
    processed_data = output.getvalue()

st.download_button(
    label="Download Prepayment Summary as Excel",
    data=processed_data,
    file_name="prepayment_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
