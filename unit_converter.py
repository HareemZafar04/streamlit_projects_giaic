import streamlit as st
from datetime import datetime

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

def convert_units(category, value, from_unit, to_unit):
    conversions = {
        "Length": {
            "Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000,
            "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084, "Inch": 39.3701
        },
        "Weight": {
            "Kilogram": 1, "Gram": 1000, "Milligram": 1e6, "Pound": 2.20462, "Ounce": 35.274
        },
        "Temperature": {
            "Celsius": lambda x: x, 
            "Fahrenheit": lambda x: (x * 9/5) + 32, 
            "Kelvin": lambda x: x + 273.15
        },
        "Time": {
            "Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400
        }
    }

    if category == "Temperature":
        # Normalize to Celsius first
        if from_unit == "Fahrenheit":
            value = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            value -= 273.15

        # Convert to target unit
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
        else:
            return value
    else:
        return value * (conversions[category][to_unit] / conversions[category][from_unit])

# UI
st.set_page_config(page_title="Unit Converter", layout="centered")
st.title("🔄 Advanced Unit Converter")

# Sidebar
st.sidebar.header("📌 Conversion Options")
categories = ["Length", "Weight", "Temperature", "Time"]
category = st.sidebar.selectbox("Choose Category", categories)

units = {
    "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
    "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Time": ["Second", "Minute", "Hour", "Day"]
}

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From Unit", units[category])
with col2:
    to_unit = st.selectbox("To Unit", units[category])

value = st.number_input("Enter Value", min_value=0.0, format="%.4f")

if st.button("Convert"):
    result = convert_units(category, value, from_unit, to_unit)
    timestamp = datetime.now().strftime("%H:%M:%S")

    st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
    st.code(f"{result:.4f}", language="text")

    # Save to history
    st.session_state.history.append(f"[{timestamp}] {value} {from_unit} ➡ {result:.4f} {to_unit}")

# Show conversion history
if st.session_state.history:
    st.subheader("📜 Conversion History")
    for item in reversed(st.session_state.history[-5:]):  # show last 5 only
        st.text(item)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

