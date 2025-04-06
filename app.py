import streamlit as st

st.set_page_config(page_title="Prepayment Certificate Calculator", layout="centered")

st.title("Prepayment Certificate Calculator")

# Input section
mda = st.text_input("MDA (Ministry, Department, or Agency)")
project_title = st.text_input("Project Title")
contractor = st.text_input("Contractor")
payment_stage = st.selectbox("Payment Stage", ["Stage Payment", "Final Payment", "Retention"])
has_retention = st.radio("Is there retention?", ["Yes", "No"]) == "Yes"
has_vat = st.radio("Is there VAT?", ["Yes", "No"]) == "Yes"

advance_payment_percentage = st.number_input("Percentage of Advance Payment (%)", min_value=0.0, max_value=100.0, step=0.5)
advance_payment_refund_percentage = st.number_input("Percentage of Advance Payment Refund (%)", min_value=0.0, max_value=100.0, step=0.5)

total_contract_sum = st.number_input("Total Contract Sum (₦)", min_value=0.0, step=1000.0)
revised_contract_sum = st.number_input("Revised Contract Sum (₦)", min_value=0.0, step=1000.0)
work_completed_to_date = st.number_input("Work Completed to Date (₦)", min_value=0.0, step=1000.0)
previous_payment = st.number_input("Previous Payment (₦)", min_value=0.0, step=1000.0)

def calculate_prepayment_certificate(
    total_contract_sum, revised_contract_sum, work_completed_to_date,
    has_retention, has_vat, advance_pct, refund_pct, previous_payment
):
    advance_payment = (advance_pct / 100) * total_contract_sum
    retention = 0.05 * work_completed_to_date if has_retention else 0
    total_net_payment = work_completed_to_date - retention
    vat = 0.075 * total_net_payment if has_vat else 0
    total_net_amount = total_net_payment + vat
    advance_refund = (refund_pct / 100) * advance_payment
    amount_due = total_net_amount - advance_refund - previous_payment

    return (
        advance_payment,
        retention,
        total_net_payment,
        vat,
        total_net_amount,
        advance_refund,
        amount_due
    )

if st.button("Calculate"):
    (
        advance_payment,
        retention_amount,
        total_net_payment,
        vat_amount,
        total_net_amount,
        advance_payment_refund,
        amount_due
    ) = calculate_prepayment_certificate(
        total_contract_sum,
        revised_contract_sum,
        work_completed_to_date,
        has_retention,
        has_vat,
        advance_payment_percentage,
        advance_payment_refund_percentage,
        previous_payment
    )

    st.subheader("Results")
    st.write(f"**Total Contract Sum**: ₦{total_contract_sum:,.2f}")
    st.write(f"**Revised Contract Sum**: ₦{revised_contract_sum:,.2f}")
    st.write(f"**Advance Payment**: ₦{advance_payment:,.2f}")
    st.write(f"**Retention**: ₦{retention_amount:,.2f}")
    st.write(f"**Total Net Payment**: ₦{total_net_payment:,.2f}")
    st.write(f"**VAT**: ₦{vat_amount:,.2f}")
    st.write(f"**Total Net Amount**: ₦{total_net_amount:,.2f}")
    st.write(f"**Advance Payment Refund**: ₦{advance_payment_refund:,.2f}")
    st.write(f"**Amount Due**: ₦{amount_due:,.2f}")
