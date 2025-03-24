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
menu = st.sidebar.selectbox(
    "Pilih Visualisasi", ["Tren PM2.5 & PM10", "Kondisi CO Tahun 2016"])

# 1. Tren PM2.5 dan PM10 tiap tahun
if menu == "Tren PM2.5 & PM10":
    st.title("Tren Konsentrasi PM2.5 dan PM10")

    # Add year range selector
    year_range = st.slider(
        "Pilih Rentang Tahun",
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max()))
    )

    # Filter data based on selected years
    filtered_df = df[(df['year'] >= year_range[0]) &
                     (df['year'] <= year_range[1])]
    yearly_trend = filtered_df.groupby("year")[['PM2.5', 'PM10']].mean()

    # Create plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=yearly_trend, markers=True)
    plt.xlabel("Tahun")
    plt.ylabel("Konsentrasi (µg/m³)")
    plt.title(
        f"Tren Rata-rata PM2.5 dan PM10 ({year_range[0]}-{year_range[1]})")
    plt.legend(["PM2.5", "PM10"])
    st.pyplot(plt)

    # Add summary statistics
    st.subheader("Statistik Ringkasan")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rata-rata PM2.5",
            f"{yearly_trend['PM2.5'].mean():.2f} µg/m³"
        )

    with col2:
        st.metric(
            "Rata-rata PM10",
            f"{yearly_trend['PM10'].mean():.2f} µg/m³"
        )

# 2. Kondisi Gas Polutan CO di Changping Tahun 2016
elif menu == "Kondisi CO Tahun 2016":
    st.title("Kondisi Gas Polutan CO di Stasiun Changping (2016)")
    df_2016 = df[df['year'] == 2016]
    df_2016.groupby(by="year").agg({"CO": ["mean"]})
    order_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['month'] =pd.Categorical(df['month'], categories=order_month, ordered=True)
    pd.pivot_table(data=df_2016,
               observed=True,
               index='month',
               columns='year',
               values=['CO'],
               aggfunc='mean')
                

    plt.figure(figsize=(10, 6))
    plt.bar(df_2016['month'], df_2016['CO'], label='CO', color='blue')
    plt.xlabel("Bulan")
    plt.ylabel("Konsentrasi CO (mg/m³)")
    plt.title("Rata-rata Konsentrasi CO per Bulan di 2016")
    st.pyplot(plt)

# Jalankan dengan: streamlit run main.py
