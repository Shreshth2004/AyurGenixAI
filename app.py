import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("AyurGenixAI_Dataset_Expanded.csv")

df = load_data()
df.columns = df.columns.str.strip()

# --- Helper Functions ---
def get_disease_info(disease, gender, age, severity):
    result = df[df["Disease"].str.lower() == disease.lower()]
    if result.empty:
        return None
    
    row = result.iloc[0]
    response = [
        f"**Disease:** {row['Disease']}",
        f"**Gender:** {gender}",
        f"**Age:** {age} years",
        f"**Severity:** {severity}",
        f"**Symptoms:** {row['Symptoms']}",
        f"**Current Medications:** {row['Current Medications']}",
        f"**Herbal Remedies:** {row['Herbal/Alternative Remedies']}",
        f"**Ayurvedic Herbs:** {row['Ayurvedic Herbs']}",
        f"**Formulation:** {row['Formulation']}",
        f"**Diet & Lifestyle:** {row['Diet and Lifestyle Recommendations']}",
        f"**Yoga / Physical Therapy:** {row['Yoga & Physical Therapy']}",
        f"**Prevention:** {row['Prevention']}",
        f"**Patient Recommendations:** {row['Patient Recommendations']}"
    ]
    return response




def get_medication_info(med_name, gender, age, severity):
    result = df[df["Current Medications"].str.contains(med_name, case=False, na=False)]
    if result.empty:
        return None
    
    diseases = result["Disease"].unique()
    response = [
        f"**Medication:** {med_name}",
        f"**Gender:** {gender}",
        f"**Age:** {age} years",
        f"**Severity:** {severity}",
        f"**Used For Diseases:** {', '.join(diseases)}",
        f"**Category:** Based on dataset usage",
        f"**Complications (if untreated):** {', '.join(result['Complications'].unique()[:3])}"
    ]
    return response

# --- Streamlit UI ---
st.title("🌿 SwasthyaAI – Drug & Disease Consultant Bot")
st.write("Ask me about a disease or a medication (dataset-driven).")

# User inputs
query = st.text_input("Enter a disease or medicine:")
gender = st.radio("Select Gender:", ["Male", "Female", "Other"])
age = st.slider("Select Age:", 1, 100, 25)
severity = st.selectbox("Select Severity Level:", ["Low", "Moderate", "High"])

if st.button("Search"):
    if query:
        disease_info = get_disease_info(query, gender, age, severity)
        med_info = get_medication_info(query, gender, age, severity)
        
        if disease_info:
            st.markdown("### 🔎 Results:")
            for point in disease_info:
                st.markdown(f"- {point}")
            st.warning("⚠ Please consult a doctor before taking any medicine.")
        
        elif med_info:
            st.markdown("### 🔎 Results:")
            for point in med_info:
                st.markdown(f"- {point}")
            st.warning("⚠ Please consult a doctor before taking any medicine.")
        
        else:
            st.error("❌ Sorry, I don’t have that specific information. Please consult a medical professional.")
    else:
        st.info("👉 Please enter a disease or medication.")
