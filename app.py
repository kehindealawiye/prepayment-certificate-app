import streamlit as st

# Function to calculate prepayment certificate details
def calculate_prepayment_certificate(total_contract_sum, revised_contract_sum, work_completed_to_date,
                                     retention, vat, advance_payment_percentage, advance_payment_refund_percentage,
                                     previous_payment):
    # Calculate advance payment
    advance_payment = total_contract_sum * (advance_payment_percentage / 100)

    # Calculate retention if applicable
    retention_amount = 0
    if retention == 'Yes':
        retention_amount = 0.05 * work_completed_to_date

    # Calculate total net payment
    total_net_payment = work_completed_to_date - retention_amount

    # Calculate VAT if applicable
    vat_amount = 0
    if vat == 'Yes':
        vat_amount = 0.075 * total_net_payment

    # Total net amount after VAT
    total_net_amount = total_net_payment + vat_amount

    # Calculate advance payment refund
    advance_payment_refund = advance_payment * (advance_payment_refund_percentage / 100)

    # Calculate amount due
    amount_due = total_net_amount - advance_payment_refund - previous_payment

    return advance_payment, retention_amount, total_net_payment, vat_amount, total_net_amount, advance_payment_refund, amount_due

# Streamlit app
def main():
    st.title("Prepayment Certificate Calculator")

    # Input fields for user
    mda = st.selectbox("Select MDA", ["Ministry of Finance", "Ministry of Economic Planning", "Ministry of Housing", "Other"])
    project_title = st.text_input("Project Title")
    contractor = st.text_input("Contractor")
    payment_stage = st.selectbox("Payment Stage", ["Stage Payment", "Final Payment", "Retention"])
    retention = st.selectbox("Is there Retention?", ["Yes", "No"])
    vat = st.selectbox("Is there VAT?", ["Yes", "No"])
    
    # Show inputs as percentages for Advance Payment and Refund
    advance_payment_percentage = st.number_input("Percentage of Advance Payment (%)", min_value=0, max_value=100, step=1)
    advance_payment_refund_percentage = st.number_input("Percentage of Advance Payment Refund (%)", min_value=0, max_value=100, step=1)

    # Show monetary amounts for contract sum and work completed
    total_contract_sum = st.number_input("Total Contract Sum (₦)", min_value=0.0, step=1000.0)
    revised_contract_sum = st.number_input("Revised Contract Sum (₦)", min_value=0.0, step=1000.0)
    work_completed_to_date = st.number_input("Work Completed to Date (₦)", min_value=0.0, step=1000.0)
    previous_payment = st.number_input("Previous Payment (₦)", min_value=0.0, step=1000.0)

    # Calculate outputs when user presses the "Calculate" button
    if st.button("Calculate"):
        advance_payment, retention_amount, total_net_payment, vat_amount, total_net_amount, advance_payment_refund, amount_due = calculate_prepayment_certificate(
            total_contract_sum, revised_contract_sum, work_completed_to_date,
            retention, vat, advance_payment_percentage, advance_payment_refund_percentage,
            previous_payment
        )

        # Display the results with the appropriate currency format
        st.write(f"**Advance Payment**: ₦{advance_payment:,.2f}")
        st.write(f"**Retention**: ₦{retention_amount:,.2f}")
        st.write(f"**Total Net Payment**: ₦{total_net_payment:,.2f}")
        st.write(f"**VAT**: ₦{vat_amount:,.2f}")
        st.write(f"**Total Net Amount**: ₦{total_net_amount:,.2f}")
        st.write(f"**Advance Payment Refund**: ₦{advance_payment_refund:,.2f}")
        st.write(f"**Amount Due**: ₦{amount_due:,.2f}")

if __name__ == "__main__":
    main()
