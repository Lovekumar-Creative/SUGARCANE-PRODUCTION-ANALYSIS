import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Title with image
st.title("🌱 Sugarcane Production Analysis Dashboard")

st.markdown("### 📊 Explore trends, compare countries, and analyze year-wise sugarcane production.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sugar-cane-production.csv")
    df = df.rename(columns={"Entity": "Country"})
    df = df.rename(columns={"Sugar cane | 00000156 || Production | 005510 || tonnes": "Production(tonnes)"})
    return df

df = load_data()

# Helper: format numbers into words
def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f} Billion"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f} Million"
    elif num >= 1_000:
        return f"{num/1_000:.2f} Thousand"
    else:
        return str(int(num))

# Show dataset preview
if st.checkbox("📂 Show raw data"):
    st.write(df.head())

# Country selection (default = India if present)
country_list = sorted(df["Country"].unique())
default_index = country_list.index("India") if "India" in country_list else 0

selected_country = st.selectbox("🌍 Select a country", country_list, index=default_index)

# Show country flag if available (using FlagCDN)
st.image(f"https://flagcdn.com/w320/{selected_country[:2].lower()}.png", width=100, caption=f"{selected_country} Flag")

# Filter data for selected country
country_df = df[df["Country"] == selected_country]

# --- Line chart with formatted y-axis ---
st.subheader(f"📈 {selected_country} - Sugarcane Production Over Years")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(country_df["Year"], country_df["Production(tonnes)"], marker="o", linestyle="-", color="green")

ax.set_title(f"Sugarcane Production in {selected_country}")
ax.set_xlabel("Year")
ax.set_ylabel("Production (tonnes)")

def format_number_axis(x, pos):
    if x >= 1_000_000_000:
        return f"{x/1_000_000_000:.1f}B"
    elif x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    elif x >= 1_000:
        return f"{x/1_000:.1f}K"
    else:
        return str(int(x))

ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_number_axis))
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# --- Country statistics ---
st.markdown("### 📊 Country Statistics")

avg_prod = country_df["Production(tonnes)"].mean()
max_prod = country_df["Production(tonnes)"].max()
min_prod = country_df["Production(tonnes)"].min()

col1, col2, col3 = st.columns(3)
col1.metric("📉 Minimum", format_number(min_prod))
col2.metric("📊 Average", format_number(avg_prod))
col3.metric("📈 Maximum", format_number(max_prod))

# --- Year-wise comparison ---
last_year = int(country_df['Year'].max())

present_year = st.number_input(
    "📅 Enter a year to check change from previous year:",
    min_value=int(country_df['Year'].min()),
    max_value=last_year,
    value=last_year,
    step=1
)

year_data = country_df[country_df['Year'] == present_year]

if not year_data.empty:
    idx = year_data.index[0]
    if idx > 0:
        current_prod = country_df.loc[idx, 'Production(tonnes)']
        prev_prod = country_df.loc[idx - 1, 'Production(tonnes)']

        if current_prod > prev_prod:
            st.success(f"✅ In {present_year}, {selected_country}'s sugarcane production **increased** compared to {present_year-1}. ({format_number(prev_prod)} → {format_number(current_prod)})")
        elif current_prod < prev_prod:
            st.error(f"❌ In {present_year}, {selected_country}'s sugarcane production **decreased** compared to {present_year-1}. ({format_number(prev_prod)} → {format_number(current_prod)})")
        else:
            st.info(f"ℹ️ In {present_year}, {selected_country}'s sugarcane production **remained the same** as {present_year-1}. ({format_number(current_prod)})")
    else:
        st.warning(f"No previous year available for {present_year}.")
else:
    st.warning("Year not found in dataset.")

# --- World average ---
world_avg = df["Production(tonnes)"].mean()
st.markdown(f"### 🌍 World Average Production: **{format_number(world_avg)} tonnes**")
