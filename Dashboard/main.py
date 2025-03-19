import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Kualitas Udara di Stasiun Changphing")
st.sidebar.title("Dashboard by Miftakhul Ma'firoh")
st.sidebar.markdown("[GitHub]()")
st.sidebar.markdown("[LinkedIn]()")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data_clean.csv")
    
    # Konversi kolom 'month' ke format angka jika masih berupa teks
    if df['month'].dtype == 'object':
        df['month'] = pd.to_datetime(df['month'], format='%B').dt.month
    
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df

df = load_data()

# Sidebar menu
st.sidebar.title("Dashboard Polusi Udara")
menu = st.sidebar.selectbox("Pilih Visualisasi", ["Tren PM2.5 & PM10", "Kondisi CO Tahun 2016"])

# 1. Tren PM2.5 dan PM10 tiap tahun
if menu == "Tren PM2.5 & PM10":
    st.title("Tren Konsentrasi PM2.5 dan PM10")
    
    yearly_trend = df.groupby("year")[['PM2.5', 'PM10']].mean()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=yearly_trend, markers=True)
    plt.xlabel("Tahun")
    plt.ylabel("Konsentrasi (µg/m³)")
    plt.title("Tren Rata-rata PM2.5 dan PM10 per Tahun")
    plt.legend(["PM2.5", "PM10"])
    st.pyplot(plt)

# 2. Kondisi Gas Polutan CO di Changping Tahun 2016
elif menu == "Kondisi CO Tahun 2016":
    st.title("Kondisi Gas Polutan CO di Stasiun Changping (2016)")
    df_2016 = df[df['year'] == 2016]
    monthly_co = df_2016.groupby("month")['CO'].mean()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_co.index, y=monthly_co.values, palette="Blues")
    plt.xlabel("Bulan")
    plt.ylabel("Konsentrasi CO (mg/m³)")
    plt.title("Rata-rata Konsentrasi CO per Bulan di 2016")
    st.pyplot(plt)

# Jalankan dengan: streamlit run main.py
