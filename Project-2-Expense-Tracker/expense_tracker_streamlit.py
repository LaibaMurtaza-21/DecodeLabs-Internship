import streamlit as st

st.set_page_config(page_title="DecodeLabs Expense Tracker", page_icon="💰")

# State initialization (persists across reruns)
if "total" not in st.session_state:
    st.session_state.total = 0.0
if "history" not in st.session_state:
    st.session_state.history = []

st.title("💰 DecodeLabs Expense Tracker")
st.caption("Project 2 — Accumulator Pattern in a Web App")

col1, col2 = st.columns([3, 1])
with col1:
    raw_input = st.text_input("Enter expense amount", key="expense_input", placeholder="e.g. 100")
with col2:
    add_clicked = st.button("Add Expense", use_container_width=True)

if add_clicked:
    try:
        expense = float(raw_input)
        if expense < 0:
            st.error("⚠️ Invalid Data: Expense cannot be negative.")
        else:
            st.session_state.total += expense
            st.session_state.history.append(expense)
            st.success(f"✔ Added ${expense:.2f}")
    except ValueError:
        st.error("⚠️ Invalid Data: Please enter a numeric value.")

st.divider()

st.metric("FINAL TOTAL SPENT", f"${st.session_state.total:.2f}")
st.write(f"Transactions recorded: **{len(st.session_state.history)}**")

if st.session_state.history:
    st.subheader("Transaction History")
    for i, amt in enumerate(st.session_state.history, start=1):
        st.write(f"{i}. ${amt:.2f}")

if st.button("🔄 Reset Tracker"):
    st.session_state.total = 0.0
    st.session_state.history = []
    st.rerun()