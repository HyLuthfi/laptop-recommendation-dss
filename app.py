import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SPK Pemilihan Laptop",
    layout="wide",
    initial_sidebar_state="expanded"
)

css_kustom = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 30px;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 10px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0px;
        padding: 10px 15px;
        color: #6B7280;
        font-weight: 600;
        font-size: 1.1rem;
        border: none !important;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        color: #111827 !important;
        border-bottom: 3px solid #111827 !important;
        background-color: transparent !important;
    }

    .metric-card {
        background-color: #FFFFFF;
        color: #111827 !important;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 32px 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }
    
    .info-card {
        background-color: #FFFFFF;
        color: #111827 !important;
        border: 1px solid #E5E7EB;
        border-left: 4px solid #111827;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }

    h1, h2, h3, h4 {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    hr {
        border-color: #E5E7EB;
        margin: 2rem 0;
    }
</style>
"""
st.markdown(css_kustom, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-top: 1rem;'>Sistem Pendukung Keputusan Pemilihan Laptop</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;'>Analisis Komparatif Algoritma Multi-Criteria Decision Making</p>", unsafe_allow_html=True)

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

st.sidebar.markdown("<h3 style='text-align: center;'>Konfigurasi Parameter</h3>", unsafe_allow_html=True)
max_price = st.sidebar.slider("Anggaran Maksimal (Euros)", min_value=200, max_value=6000, value=1000, step=50)
min_ram = st.sidebar.selectbox("Kapasitas RAM Minimal (GB)", [4, 8, 16, 32, 64], index=1)
top_n = st.sidebar.slider("Populasi Alternatif Evaluasi", min_value=5, max_value=20, value=10)

dataset_filter = df[(df['Price (Euros)'] <= max_price) & (df['RAM'] >= min_ram)].copy()

if len(dataset_filter) < top_n:
    top_n = len(dataset_filter)

if len(dataset_filter) == 0:
    st.error("Data observasi tidak ditemukan berdasarkan kriteria spesifikasi tersebut.")
    st.stop()

dataframe_laptop = dataset_filter[['Alternatif', 'Price (Euros)', 'RAM', 'Storage (GB)', 'Weight', 'Screen Size']].head(top_n).copy()
dataframe_laptop.columns = ['Alternatif', 'Harga', 'RAM', 'Storage', 'Berat', 'Layar']

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

tab_dashboard, tab_saw, tab_topsis, tab_waspas, tab_visual = st.tabs([
    "Dashboard Utama",
    "Analisis SAW",
    "Analisis TOPSIS",
    "Analisis WASPAS",
    "Visualisasi Komparatif"
])

with tab_dashboard:
    st.markdown("<div class='info-card'><b>Dataset Alternatif Evaluasi:</b> Tabel spesifikasi teknis kandidat laptop berdasarkan parameter filter. Kumpulan data ini mendasari penetapan Matriks Keputusan Utama.</div>", unsafe_allow_html=True)
    st.dataframe(dataframe_laptop, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Laporan Perbandingan Peringkat Akhir</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><h3 style='color: #374151; font-size: 1.2rem; margin-bottom: 1rem;'>Metode SAW</h3></div>", unsafe_allow_html=True)
        df_saw = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor': nilai_akhir_saw}).sort_values('Skor', ascending=False).reset_index(drop=True)
        df_saw.index = df_saw.index + 1
        st.dataframe(df_saw, use_container_width=True)
    with col2:
        st.markdown("<div class='metric-card'><h3 style='color: #374151; font-size: 1.2rem; margin-bottom: 1rem;'>Metode TOPSIS</h3></div>", unsafe_allow_html=True)
        df_topsis = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor': kedekatan_relatif}).sort_values('Skor', ascending=False).reset_index(drop=True)
        df_topsis.index = df_topsis.index + 1
        st.dataframe(df_topsis, use_container_width=True)
    with col3:
        st.markdown("<div class='metric-card'><h3 style='color: #374151; font-size: 1.2rem; margin-bottom: 1rem;'>Metode WASPAS</h3></div>", unsafe_allow_html=True)
        df_waspas = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor': nilai_akhir_waspas}).sort_values('Skor', ascending=False).reset_index(drop=True)
        df_waspas.index = df_waspas.index + 1
        st.dataframe(df_waspas, use_container_width=True)

with tab_saw:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Penjabaran Metode Simple Additive Weighting (SAW)</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<b>Langkah 1: Matriks Keputusan Ternormalisasi (R)</b>", unsafe_allow_html=True)
    st.markdown("Proses normalisasi berdasarkan identitas atribut (Cost atau Benefit) untuk menyelaraskan interval matriks.")
    df_norm_saw = pd.DataFrame(matriks_normalisasi_saw, columns=nama_kriteria, index=nama_alternatif)
    st.dataframe(df_norm_saw, use_container_width=True)
    
    st.markdown("<br><b>Langkah 2: Perhitungan Nilai Preferensi (V)</b>", unsafe_allow_html=True)
    st.markdown("Perkalian aditif antara matriks ternormalisasi dan nilai persentase bobot kriteria yang menghasilkan skor peringkat.")
    df_hasil_saw = pd.DataFrame({'Nilai Preferensi': nilai_akhir_saw}, index=nama_alternatif).sort_values('Nilai Preferensi', ascending=False)
    st.dataframe(df_hasil_saw, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_topsis:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Penjabaran Metode TOPSIS</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<b>Langkah 1: Matriks Keputusan Ternormalisasi Terbobot (Y)</b>", unsafe_allow_html=True)
    df_norm_topsis = pd.DataFrame(matriks_terbobot_topsis, columns=nama_kriteria, index=nama_alternatif)
    st.dataframe(df_norm_topsis, use_container_width=True)
    
    st.markdown("<br><b>Langkah 2: Penentuan Solusi Ideal Ekstrem</b>", unsafe_allow_html=True)
    df_ideal = pd.DataFrame([solusi_ideal_positif, solusi_ideal_negatif], columns=nama_kriteria, index=['Solusi Ideal Positif (A+)', 'Solusi Ideal Negatif (A-)'])
    st.dataframe(df_ideal, use_container_width=True)
    
    st.markdown("<br><b>Langkah 3: Perhitungan Kedekatan Relatif</b>", unsafe_allow_html=True)
    st.markdown("Distribusi matriks jarak Euclidean (D+ dan D-) untuk mengkalkulasi persentase kedekatan opsi terhadap solusi sempurna.")
    df_hasil_topsis = pd.DataFrame({'Jarak (D+)': jarak_positif, 'Jarak (D-)': jarak_negatif, 'Kedekatan Relatif': kedekatan_relatif}, index=nama_alternatif).sort_values('Kedekatan Relatif', ascending=False)
    st.dataframe(df_hasil_topsis, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_waspas:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Penjabaran Metode WASPAS</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<b>Langkah 1: Komparasi Weighted Sum Model dan Weighted Product Model</b>", unsafe_allow_html=True)
    st.markdown("Ekstraksi skor evaluasi ganda dengan menggunakan integrasi model optimasi aditif dan eksponensial.")
    df_wsm_wpm = pd.DataFrame({'Skor WSM': nilai_wsm, 'Skor WPM': nilai_wpm}, index=nama_alternatif)
    st.dataframe(df_wsm_wpm, use_container_width=True)
    
    st.markdown("<br><b>Langkah 2: Agregasi Kombinasi Preferensi</b>", unsafe_allow_html=True)
    st.markdown("Agregasi final dengan memanfaatkan parameter keseimbangan dinamis sebesar 0.5.")
    df_hasil_waspas = pd.DataFrame({'Skor Akhir Kombinasi': nilai_akhir_waspas}, index=nama_alternatif).sort_values('Skor Akhir Kombinasi', ascending=False)
    st.dataframe(df_hasil_waspas, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_visual:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Distribusi Grafik Pemeringkatan</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    fig, axis = plt.subplots(1, 3, figsize=(18, 6))
    warna_palet = ['#0F172A', '#1E293B', '#334155', '#475569', '#64748B', '#94A3B8', '#CBD5E1', '#E2E8F0', '#F1F5F9', '#F8FAFC'] * 3
    daftar_metode = [('SAW', nilai_akhir_saw), ('TOPSIS', kedekatan_relatif), ('WASPAS', nilai_akhir_waspas)]

    for index_ax, (nama_metode, skor_metode) in enumerate(daftar_metode):
        urutan = np.argsort(-skor_metode)
        label_urut = [nama_alternatif[k] for k in urutan]
        skor_urut = skor_metode[urutan]
        warna_urut = [warna_palet[k] for k in urutan]
        axis[index_ax].barh(label_urut[::-1], skor_urut[::-1], color=warna_urut[::-1], edgecolor='#111827')
        axis[index_ax].set_title(f'Peringkat {nama_metode}', fontsize=14, fontweight='bold', color='#111827')
        axis[index_ax].set_xlabel('Nilai Skoring', fontsize=12, color='#374151')
        axis[index_ax].tick_params(axis='y', labelsize=10)
        axis[index_ax].grid(axis='x', linestyle='--', alpha=0.5)
        for idx_bar, v_bar in enumerate(skor_urut[::-1]):
            axis[index_ax].text(v_bar + (0.01 * np.max(skor_urut)), idx_bar, f'{v_bar:.4f}', va='center', fontsize=9, color='#111827', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
