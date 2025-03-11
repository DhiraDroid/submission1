import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
file_path = r"C:\Users\LENOVO\Downloads\DBS\submission\dashboard\main_data.csv"
bike_data = pd.read_csv(file_path)

# Konversi kolom tanggal jika diperlukan
bike_data['dteday'] = pd.to_datetime(bike_data['dteday'])

# Sidebar untuk pemilihan rentang tanggal
st.sidebar.title("Rentang Waktu")
start_date = st.sidebar.date_input("Mulai", bike_data['dteday'].min())
end_date = st.sidebar.date_input("Akhir", bike_data['dteday'].max())

st.sidebar.caption('Pilih tanggal dalam rentang 1 Januari 2011 s.d. 31 Desember 2012 ')

# Filter data berdasarkan tanggal
filtered_data = bike_data[(bike_data['dteday'] >= pd.to_datetime(start_date)) &
                          (bike_data['dteday'] <= pd.to_datetime(end_date))]

if filtered_data.empty:
    st.warning("Tidak ada data dalam rentang ini.")
    filtered_data = bike_data.iloc[:0]  # Set dataset kosong jika di luar rentang

# Header
st.title("Proyek Analisis Data: Bike-Sharing-Dataset")
st.write("""
**Nama:** Aldhira Calysta Athalia Siahaan  
**Email:** aldhirathalia@student.ub.ac.id  
**ID Dicoding:** MC006D5X2418  
""")


# Daily Count of Total Rental Bikes
st.header("Daily Count of Total Rental Bikes")

col1, col2, col3 = st.columns(3)

with col1:
    total_rents = filtered_data['cnt'].sum()
    st.metric("Total Rents", total_rents)

with col2:
    avg_temp = filtered_data['temp'].mean() * 41  # Denormalisasi suhu
    st.metric("Average Temperature (°C)", round(avg_temp, 2))
with col3:    
    time_span = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1
    st.metric("Time Span (days)", time_span)



# Total Rents Chart
fig, ax = plt.subplots(figsize=(10,5))  # Ukuran grafik agar lebih proporsional
ax.plot(filtered_data['dteday'], filtered_data['cnt'], marker='o', linestyle='-', 
        markersize=3, linewidth=0.8, alpha=0.7)  # Titik lebih kecil dan garis lebih tipis

ax.set_title("Total Rents Over Time", fontsize=14)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Total Rents", fontsize=12)

plt.xticks(rotation=45)  # Agar label tanggal tidak bertumpuk
plt.grid(True, linestyle='--', alpha=0.5)  # Grid untuk memperjelas tren

st.pyplot(fig)

# Total Customer Status Chart
fig, ax = plt.subplots()
filtered_data[['cnt', 'casual', 'registered']].sum().plot(kind='bar', ax=ax, color=['blue', 'green', 'red'])
ax.set_title("Total Customer Status")
ax.set_ylabel("Count (juta)")
st.pyplot(fig)

# Customer Demographics
st.header("Customer Demographics")
st.subheader("Number of Customers by Category")

fig, axes = plt.subplots(3, 2, figsize=(12, 10))

# By Season
filtered_data.groupby('season')['cnt'].sum().plot(kind='bar', ax=axes[0, 0], color='c')
axes[0, 0].set_title("By Season")

# By Month
filtered_data.groupby('mnth')['cnt'].sum().plot(kind='bar', ax=axes[0, 1], color='m')
axes[0, 1].set_title("By Month")

# By Holiday
filtered_data.groupby('holiday')['cnt'].sum().plot(kind='bar', ax=axes[1, 0], color='orange')
axes[1, 0].set_title("By Holiday")

# By Weathersit
filtered_data.groupby('weathersit')['cnt'].sum().plot(kind='bar', ax=axes[1, 1], color='purple')
axes[1, 1].set_title("By Weathersit")

# By Temp
filtered_data.groupby('temp')['cnt'].sum().plot(
    kind='line', ax=axes[2, 0], color='red', marker='o', markersize=3, linewidth=0.5
)
axes[2, 0].set_title("By Temp")

# By Working Day
filtered_data.groupby('workingday')['cnt'].sum().plot(kind='bar', ax=axes[2, 1], color='g')
axes[2, 1].set_title("By Working Day")

# Atur jarak antar subplot
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# Tampilkan di Streamlit
st.pyplot(fig)

# Penjelasan tentang Dataset & Grafik
st.write("""
### Analisis Pola Penyewaan Sepeda
Dataset ini mencatat jumlah penyewaan sepeda berdasarkan faktor musim, bulan, hari kerja, cuaca, dan suhu.  
Berikut adalah hasil analisis yang diperoleh dari grafik:

1. **Musim (Season)**  
   - Penyewaan sepeda **paling tinggi** terjadi pada **musim gugur (Fall, 3)**, sedangkan **paling rendah** pada **musim semi (Spring, 1)**.  
   - Detail kategori musim:  
     - **1** → Musim Semi  
     - **2** → Musim Panas  
     - **3** → Musim Gugur  
     - **4** → Musim Dingin  

2. **Bulan (Month)**  
   - Pola bulanan menunjukkan peningkatan penyewaan sepeda dari awal tahun, **memuncak pada bulan Juni - September (6-9)**, lalu menurun menjelang akhir tahun.

3. **Hari Libur (Holiday)**  
   - Penyewaan sepeda jauh lebih tinggi pada **hari biasa (0: bukan hari libur)** dibandingkan pada hari libur **(1: hari libur)**.

4. **Kondisi Cuaca (Weathersit)**  
   - Cuaca yang cerah dan berawan ringan **(Kategori 1)** memiliki jumlah penyewaan tertinggi.  
   - Saat cuaca mendung atau berkabut **(Kategori 2)**, penyewaan mulai menurun.  
   - Cuaca hujan ringan atau salju **(Kategori 3)** menyebabkan penurunan signifikan dalam jumlah penyewaan.  
   - Kondisi ekstrem seperti hujan deras atau salju lebat **(Kategori 4)** menyebabkan penyewaan sangat minim.  
   - Detail kategori cuaca:  
     - **1** → Cerah, sedikit berawan  
     - **2** → Berawan, kabut  
     - **3** → Hujan ringan, salju ringan  
     - **4** → Hujan deras, badai salju  

5. **Suhu (Temp)**  
   - Penyewaan meningkat seiring kenaikan suhu, tetapi saat suhu **terlalu tinggi**, jumlah penyewaan sedikit menurun.

6. **Hari Kerja (Working Day)**  
   - Penyewaan lebih tinggi pada **hari kerja (1)** dibandingkan akhir pekan atau hari libur **(0)**.

### Kesimpulan
Dari analisis ini, terlihat bahwa **musim, cuaca, dan hari kerja sangat memengaruhi pola penyewaan sepeda**.  
Sebagai strategi bisnis, pemilik rental sepeda dapat **menambah stok saat musim gugur dan bulan dengan permintaan tinggi**, serta **menyesuaikan jumlah unit saat cuaca ekstrem**.
""")


# Analisis Tambahan: Clustering
st.header("Analisis Tambahan: Binning Clustering")
hour_bins = [50, 200, 500, 900, float('inf')]
hour_labels = ['Sepi', 'Normal', 'Ramai', 'Sangat Ramai']

filtered_data['cnt_binned'] = pd.cut(filtered_data['cnt'], bins=hour_bins, labels=hour_labels)
hour_binned_count = filtered_data['cnt_binned'].value_counts()
st.bar_chart(hour_binned_count)

st.write("""
Grafik ini menunjukkan hasil clustering berdasarkan jumlah penyewaan sepeda.  
Kategori clustering dan rentangnya:
- **Sepi**: Penyewaan antara **50 - 200** sepeda.
- **Normal**: Penyewaan antara **201 - 500** sepeda.
- **Ramai**: Penyewaan antara **501 - 900** sepeda.
- **Sangat Ramai**: Penyewaan lebih dari **900** sepeda.

Kategori ini membantu dalam memahami pola penggunaan sepeda dan membuat keputusan terkait layanan penyewaan.
""")


st.caption('Copyright © MC006D5X2418-Aldhira Calysta Athalia Siahaan')

