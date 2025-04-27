import streamlit as st
from data import *

def judul():
    st.title("Dashboard Covid-19 Indonesia")
    st.write("Selamat Datang di Dashboard Interaktif Untuk Menganalisis Data Covid-19 Di Indonesia")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman",["Home","Halaman Data"])
if menu == "Home":
    judul()
    year = select_year(key="year_home")
    df = load_data()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    kolom1(df_filtered)
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)
    
elif menu == "Halaman Data":
    judul()
    year = select_year(key="year_data")
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)
