import streamlit as st
import pandas as pd
import plotly.express as px  

# Load data
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv") 
    df = df[df["Location"] != "Indonesia"]
    return df

# Filter data berdasarkan tahun
def filter_data(df, year=None, locations=None):
    df['Date'] = pd.to_datetime(df['Date'])  
    if year is not None:
        df = df[df["Date"].dt.year == year]
    if locations:
        df = df[df["Location"].isin(locations)]  
    return df



# Select location
def select_location(df, key="location"):
    return st.sidebar.multiselect(
        "Pilih Provinsi 📍",
        options=sorted(df["Location"].unique()), 
        default=None,
        key=key
    )


# Pilihan tahun
def select_year(key="year"):
    return st.sidebar.selectbox(
        "Pilih Tahun",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else x,
        key=key
    )

# Tampilkan data
def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia")
    st.dataframe(df_selected.head(10))

    # Statistik deskriptif
    st.subheader('Statistik Deskriptif Dataset')
    st.write(df_selected.describe())

# Total kasus
def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

# Total kematian
def total_death(df):
    total_mati = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_mati['Total Deaths'].sum()

# Total sembuh
def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

# Tampilkan 3 metrik
def kolom1(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus", value=kasus + 37, delta="+37", delta_color="inverse")
    col2.metric(label="Total Kematian", value=kematian + 20, delta="+20", delta_color="inverse")
    col3.metric(label="Total Sembuh", value=sembuh + 75, delta="+75", delta_color="normal")

# Pie chart: Perbandingan kematian dan kesembuhan
def pie_chart1(df):
    total_mati = total_death(df)
    total_hidup = total_recovery(df)

    data = pd.DataFrame({
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_hidup]
    })

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian vs Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#ff6459', '#4de89f']  # merah untuk meninggal, hijau untuk sembuh
    )

    st.plotly_chart(fig, use_container_width=True)

# Bar Chart
def bar_chart1(df):
    # Ambil data terakhir per provinsi
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    # Ambil 5 provinsi dengan kematian terbanyak
    top5 = df_last.nlargest(5, 'Total Deaths')

    # Buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='Top 5 Provinsi dengan Kematian Teringgi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

# Bar Chart
def bar_chart2(df):
    # Ambil data terakhir per provinsi
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    # Ambil 5 provinsi dengan kesembuhan terbanyak
    top5 = df_last.nlargest(5, 'Total Recovered')

    # Buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='greens',
        title='Top 5 Provinsi dengan Kesembuhan Teringgi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

# Map chart
def map_chart(df, year=None):
    # Konversi tanggal
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter berdasarkan tahun jika dipilih
    if year:
        df = df[df['Date'].dt.year == year]

    # Agregasi data per lokasi
    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    # Validasi data
    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan di peta.")
        return

    # Buat map chart
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},  # Fokus Indonesia
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )

    # Gunakan style default Mapbox
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)
