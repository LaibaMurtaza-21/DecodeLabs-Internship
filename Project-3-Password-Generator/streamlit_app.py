"""
DecodeLabs - Project 3: Random Password Generator (Streamlit version)
Same core logic as password_generator.py, wrapped in a web UI.
"""

import secrets
import string
import streamlit as st


def build_character_pool(use_letters, use_digits, use_symbols):
    pool = ""
    if use_letters:
        pool += string.ascii_letters
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation
    return pool


def generate_password(length, pool):
    password_chars = [secrets.choice(pool) for _ in range(length)]
    return ''.join(password_chars)


def estimate_entropy(length, pool_size):
    import math
    return round(length * math.log2(pool_size), 1) if pool_size > 0 else 0


st.set_page_config(page_title="Secure Password Generator", page_icon="🔐")

st.title("🔐 DecodeLabs Secure Password Generator")
st.caption("Built with Python's `secrets` module — cryptographically secure, not just random.")

length = st.slider("Password length", min_value=8, max_value=64, value=16)

col1, col2, col3 = st.columns(3)
with col1:
    use_letters = st.checkbox("Letters (A-z)", value=True)
with col2:
    use_digits = st.checkbox("Digits (0-9)", value=True)
with col3:
    use_symbols = st.checkbox("Symbols (@#$...)", value=False)

if st.button("Generate Password", type="primary"):
    pool = build_character_pool(use_letters, use_digits, use_symbols)

    if not pool:
        st.error("Select at least one character type.")
    else:
        password = generate_password(length, pool)
        st.success("Password generated!")
        st.code(password, language=None)

        entropy = estimate_entropy(length, len(pool))
        st.metric("Estimated entropy", f"{entropy} bits")

        if entropy < 60:
            st.warning("Weak — consider increasing length or enabling more character types.")
        elif entropy < 100:
            st.info("Reasonable strength for everyday use.")
        else:
            st.success("Strong — suitable for high-security accounts.")

st.divider()
st.caption("NIST SP 800-63-4 (2024) recommends prioritizing length over forced complexity.")
