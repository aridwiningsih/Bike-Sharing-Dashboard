import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Memuat data
days_file_path = "dayClean_df.csv"
days_df = pd.read_csv(days_file_path)

# Memuat Datetime
days_df["date"] = pd.to_datetime(days_df["date"])

# Mendefinisikan fungsi
def create_total_bike_sharing(day_df):
    result = day_df.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return result["count"].sum()

def create_total_registered_user(day_df):
    result = day_df.groupby(by="date").agg({
        "registered": "sum"
    })
    result = result.reset_index()
    return result["registered"].sum()

def create_total_casual_user(day_df):
    result = day_df.groupby(by="date").agg({
        "casual": "sum"
    })
    result = result.reset_index()
    return result["casual"].sum()

def create_user_bulanan_df(day_df):
    user_bulanan_df = day_df.resample(rule='M', on='date').agg({
        "unregistered": "sum",
        "casual": "sum",
        "count": "sum"
    })
    user_bulanan_df = user_bulanan_df.reset_index()
    user_bulanan_df.index = user_bulanan_df.index.strftime('%b-%y')
    user_bulanan_df.rename(columns={
        "date": "yearmonth",
        "count": "count",
        "unregistered": "unregistered",
        "casual": "registered"
    }, inplace=True)

    return user_bulanan_df

def datefilter_range(days_df, start_date, end_date):
    return days_df[(days_df["date"] >= str(start_date)) & (days_df["date"] <= str(end_date))]

# Membuat Judul Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard",
                   page_icon=":sparkles:",
                   layout="wide")

# Membuat komponen filter (range)
min_date = days_df["date"].min()
max_date = days_df["date"].max()

# Membuat Sidebar
with st.sidebar:
    # add logo
    st.image("../logo/image.png")
    st.markdown("<h1 style='text-align: center;'>Date Filter</h1>", unsafe_allow_html=True)

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Select Date Range:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menghubungkan filter dengan main_days_df
main_days_df = datefilter_range(days_df, start_date, end_date)

# Halaman utama
st.title(":sparkles: Bike Sharing Dashboard :sparkles:")
st.markdown("##")

# Membuat Kolom
col1, col2, col3 = st.columns(3)

with col1:
    total_bike_sharing = main_days_df['count'].sum()
    st.metric("Total User", value=total_bike_sharing)
with col2:
    total_casual_user = main_days_df['casual'].sum()
    st.metric("Total Casual User", value=total_casual_user)
with col3:
    total_registered_user = main_days_df['registered'].sum()
    st.metric("Total Registered User", value=total_registered_user)

# Visualisasi data pertanyaaan 1
st.subheader("Pengaruh Cuaca terhadap Jumlah Pengguna Sepeda")
color_list = ["#F4D0D0", "#BAC9CE", "#D1A38C"] # Daftar warna bar yang akan digunakan 
fig, ax = plt.subplots()
sns.barplot( # Membuat bar
    y='count',
    x='weather_cond',
    data=days_df,
    hue='weather_cond',  # Assign 'weather_cond' ke parameter 'hue'
    palette=color_list,
    legend=False  # Set 'legend=False'
)

plt.title('Pengaruh Cuaca terhadap Jumlah Pengguna Sepeda')
plt.xlabel(' ')
plt.ylabel('Jumlah Pengguna Sepeda')

st.pyplot(fig)

#Visualisasi data pertanyaan 2
st.subheader("Jumlah Pengguna Rental Sepeda per Bulan dalam Setahun")
months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] # Definisikan urutan bulan
days_df['month'] = pd.Categorical(days_df['month'], categories=months_order, ordered=True) # Ubah kolom 'month' menjadi kategori dengan urutan yang ditentukan

grouped_year = days_df.groupby(['year', 'month'])['count'].mean().reset_index(name='counts') # Mengelompokkan data
fig, ax = plt.subplots(figsize=(12, 7)) # Plotting

for year, group in grouped_year.groupby('year'): # Loop melalui nilai 'year' yang unik
    ax.plot(group['month'], group['counts'], marker='o', label=f'Year: {year}')

ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Pengguna')
ax.set_title('Jumlah Pengguna Rental Sepeda per Bulan dalam Setahun')
plt.legend(title='Year', loc='upper right')

st.pyplot(fig)

# Menambahkan copyright
st.caption('Copyright (c) Ari Dwiningsih 2024')