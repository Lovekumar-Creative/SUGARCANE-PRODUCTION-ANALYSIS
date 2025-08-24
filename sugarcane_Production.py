import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("🌱 Sugarcane Production Analysis")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sugar-cane-production.csv")
    df = df.rename(columns={"Entity": "Country"})
    df = df.rename(columns={"Sugar cane | 00000156 || Production | 005510 || tonnes": "Production(tonnes)"})
    return df

df = load_data()

# Show dataset preview
if st.checkbox("Show raw data"):
    st.write(df.head())

# Country selection
country_list = df["Country"].unique()
selected_country = st.selectbox("Select a country", sorted(country_list))

# Filter data for selected country
country_df = df[df["Country"] == selected_country]

# Line chart
st.subheader(f"{selected_country} - Sugarcane Production Over Years")
st.line_chart(country_df.set_index("Year")["Production(tonnes)"])

# World average
world_avg = round(df["Production(tonnes)"].mean(), 2)
st.metric("🌍 World Average Production", f"{world_avg} tonnes")

# Country statistics
avg_prod = round(country_df["Production(tonnes)"].mean(), 2)
max_prod = round(country_df["Production(tonnes)"].max(), 2)
min_prod = round(country_df["Production(tonnes)"].min(), 2)

st.write(f"**Average Production of {selected_country}:** {avg_prod} tonnes")
st.write(f"**Maximum Production of {selected_country}:** {max_prod} tonnes")
st.write(f"**Minimum Production of {selected_country}:** {min_prod} tonnes")

# Year-wise increase analysis
st.subheader(f"Years when {selected_country} produced more than previous year")
years_increased = []
data = country_df.values
for i in range(1, len(data)):
    if data[i][3] > data[i-1][3]:
        years_increased.append(f"{data[i][2]} more than {data[i-1][2]}")

if years_increased:
    st.write(years_increased)
else:
    st.write("No year with an increase compared to the previous year.")
