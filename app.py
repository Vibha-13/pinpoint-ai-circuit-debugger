import streamlit as st
import json
import os

# Load circuit rules
with open("circuit_rules.json", "r") as file:
    circuit_rules = json.load(file)

st.set_page_config(page_title="PinPoint - AI Circuit Debugger", layout="centered")

# App title
st.title("🔌 PinPoint - AI Circuit Debugger")
st.write("Validate your circuit wiring and get instant feedback!")

# Select circuit
selected_circuit = st.selectbox("Select a circuit to validate:", list(circuit_rules.keys()))

st.markdown("---")

# User input
user_connections = st.text_area(
    "Enter your wiring (one connection per line):",
    placeholder="Example:\nArduino Pin 13 -> LED Anode\nLED Cathode -> Resistor\nResistor -> GND"
)

# Validate button
if st.button("Validate"):
    expected_connections = circuit_rules[selected_circuit]["connections"]
    expected_set = {f"{c['from']} -> {c['to']}" for c in expected_connections}

    user_lines = [line.strip() for line in user_connections.split("\n") if line.strip()]
    user_set = set(user_lines)

    missing = expected_set - user_set
    extra = user_set - expected_set

    if not missing and not extra:
        st.success("✅ Perfect! Your wiring matches the expected connections.")
    else:
        if missing:
            st.error("⚠ Missing connections:")
            for m in missing:
                st.write(f"- {m}")
        if extra:
            st.warning("⚠ Extra or incorrect connections:")
            for e in extra:
                st.write(f"- {e}")

    # Show notes
    st.info(circuit_rules[selected_circuit]["notes"])
