import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SPK Pemilihan Laptop", page_icon="💻", layout="wide")

st.title("💻 Sistem Pendukung Keputusan Pemilihan Laptop")
st.markdown("Aplikasi web ini menggunakan algoritma **SAW, TOPSIS, dan WASPAS** untuk memberikan rekomendasi laptop terbaik berdasarkan dataset *Laptop Price* dari Kaggle.")

@st.cache_data
def load_data():
    file_dataset = 'dataset_laptop_lengkap.csv'
    dataset_mentah = pd.read_csv(file_dataset, encoding='latin-1')
    
    dataset_mentah['Price (Euros)'] = dataset_mentah['Price (Euros)'].astype(str).str.replace(',', '.').astype(float)
    dataset_mentah['RAM'] = dataset_mentah['RAM'].astype(str).str.replace('GB', '').astype(int)
    dataset_mentah['Weight'] = dataset_mentah['Weight'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    storage_mentah = dataset_mentah[' Storage'].astype(str).str.replace('TB', '000GB')
    dataset_mentah['Storage (GB)'] = storage_mentah.str.extract(r'(\d+)').astype(float)
    dataset_mentah['Screen Size'] = dataset_mentah['Screen Size'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    dataset_mentah['Alternatif'] = dataset_mentah['Manufacturer'] + ' ' + dataset_mentah['Model Name']
    return dataset_mentah

df = load_data()

st.sidebar.header("⚙️ Filter Kebutuhan Anda")
max_price = st.sidebar.slider("Budget Maksimal (Euros)", min_value=200, max_value=6000, value=1000, step=50)
min_ram = st.sidebar.selectbox("Minimal RAM (GB)", [4, 8, 16, 32, 64], index=1)
top_n = st.sidebar.slider("Jumlah Alternatif Diuji (Top N)", min_value=5, max_value=20, value=10)

dataset_filter = df[(df['Price (Euros)'] <= max_price) & (df['RAM'] >= min_ram)].copy()

if len(dataset_filter) < top_n:
    st.sidebar.warning(f"Hanya {len(dataset_filter)} laptop ditemukan dengan kriteria tersebut.")
    top_n = len(dataset_filter)

if len(dataset_filter) == 0:
    st.error("❌ Tidak ada laptop yang memenuhi kriteria filter Anda. Silakan longgarkan filter di sidebar (Naikkan budget atau turunkan RAM).")
    st.stop()

dataframe_laptop = dataset_filter[['Alternatif', 'Price (Euros)', 'RAM', 'Storage (GB)', 'Weight', 'Screen Size']].head(top_n).copy()
dataframe_laptop.columns = ['Alternatif', 'Harga', 'RAM', 'Storage', 'Berat', 'Layar']

st.subheader("📋 Dataset Alternatif (Telah Difilter)")
st.dataframe(dataframe_laptop, use_container_width=True)

matriks_keputusan = dataframe_laptop.iloc[:, 1:].values
bobot_kriteria = np.array([0.35, 0.20, 0.20, 0.15, 0.10])
status_kriteria = ['cost', 'benefit', 'benefit', 'cost', 'benefit']
nama_kriteria = ['Harga', 'RAM', 'Storage', 'Berat', 'Layar']
nama_alternatif = dataframe_laptop['Alternatif'].values
jumlah_kolom = matriks_keputusan.shape[1]

matriks_normalisasi_saw = np.zeros_like(matriks_keputusan, dtype=float)
for kolom in range(jumlah_kolom):
    data_kolom = matriks_keputusan[:, kolom]
    if status_kriteria[kolom] == 'benefit':
        matriks_normalisasi_saw[:, kolom] = data_kolom / np.max(data_kolom)
    else:
        matriks_normalisasi_saw[:, kolom] = np.min(data_kolom) / data_kolom

nilai_akhir_saw = np.sum(matriks_normalisasi_saw * bobot_kriteria, axis=1)

pembagi_topsis = np.sqrt(np.sum(matriks_keputusan**2, axis=0))
matriks_normalisasi_topsis = matriks_keputusan / pembagi_topsis
matriks_terbobot_topsis = matriks_normalisasi_topsis * bobot_kriteria

solusi_ideal_positif = np.zeros(jumlah_kolom)
solusi_ideal_negatif = np.zeros(jumlah_kolom)

for kolom in range(jumlah_kolom):
    if status_kriteria[kolom] == 'benefit':
        solusi_ideal_positif[kolom] = np.max(matriks_terbobot_topsis[:, kolom])
        solusi_ideal_negatif[kolom] = np.min(matriks_terbobot_topsis[:, kolom])
    else:
        solusi_ideal_positif[kolom] = np.min(matriks_terbobot_topsis[:, kolom])
        solusi_ideal_negatif[kolom] = np.max(matriks_terbobot_topsis[:, kolom])

jarak_positif = np.sqrt(np.sum((matriks_terbobot_topsis - solusi_ideal_positif)**2, axis=1))
jarak_negatif = np.sqrt(np.sum((matriks_terbobot_topsis - solusi_ideal_negatif)**2, axis=1))
kedekatan_relatif = jarak_negatif / (jarak_negatif + jarak_positif)

nilai_wsm = np.sum(matriks_normalisasi_saw * bobot_kriteria, axis=1)
nilai_wpm = np.prod(matriks_normalisasi_saw ** bobot_kriteria, axis=1)
konstanta_lambda = 0.5
nilai_akhir_waspas = (konstanta_lambda * nilai_wsm) + ((1 - konstanta_lambda) * nilai_wpm)

st.write("---")
st.subheader("🏆 Peringkat Laptop Terbaik")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Top SAW**")
    df_saw = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor': nilai_akhir_saw}).sort_values('Skor', ascending=False).reset_index(drop=True)
    df_saw.index = df_saw.index + 1
    st.dataframe(df_saw.head(5), use_container_width=True)
with col2:
    st.success("**Top TOPSIS**")
    df_topsis = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor': kedekatan_relatif}).sort_values('Skor', ascending=False).reset_index(drop=True)
    df_topsis.index = df_topsis.index + 1
    st.dataframe(df_topsis.head(5), use_container_width=True)
with col3:
    st.warning("**Top WASPAS**")
    df_waspas = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor': nilai_akhir_waspas}).sort_values('Skor', ascending=False).reset_index(drop=True)
    df_waspas.index = df_waspas.index + 1
    st.dataframe(df_waspas.head(5), use_container_width=True)

st.write("---")
st.subheader("📊 Visualisasi Perbandingan Metode")

fig, axis = plt.subplots(1, 3, figsize=(18, 5))
warna_grafik = ['#2c3e50', '#e74c3c', '#27ae60', '#f39c12', '#8e44ad', '#2980b9', '#d35400', '#c0392b', '#1abc9c', '#34495e'] * 3
daftar_metode = [('SAW', nilai_akhir_saw), ('TOPSIS', kedekatan_relatif), ('WASPAS', nilai_akhir_waspas)]

for index_ax, (nama_metode, skor_metode) in enumerate(daftar_metode):
    urutan = np.argsort(-skor_metode)
    label_urut = [nama_alternatif[k] for k in urutan]
    skor_urut = skor_metode[urutan]
    warna_urut = [warna_grafik[k] for k in urutan]
    axis[index_ax].barh(label_urut[::-1], skor_urut[::-1], color=warna_urut[::-1], edgecolor='black')
    axis[index_ax].set_title(f'Peringkat Metode {nama_metode}')
    axis[index_ax].set_xlabel('Skor Akhir')
    for idx_bar, v_bar in enumerate(skor_urut[::-1]):
        axis[index_ax].text(v_bar + 0.005, idx_bar, f'{v_bar:.4f}', va='center', fontsize=9)

plt.tight_layout()
st.pyplot(fig)
