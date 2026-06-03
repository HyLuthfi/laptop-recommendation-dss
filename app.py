import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SPK Pemilihan Laptop",
    layout="wide",
    initial_sidebar_state="expanded"
)

css_premium = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Beautiful Gradient Header */
    .premium-title {
        background: linear-gradient(135deg, #0F172A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        font-size: 3rem !important;
        letter-spacing: -0.05rem;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }

    .premium-subtitle {
        text-align: center;
        color: #64748B;
        font-weight: 400;
        font-size: 1.15rem;
        margin-bottom: 3.5rem;
        letter-spacing: 0.02rem;
    }

    /* Animated Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 30px 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #F1F5F9;
        position: relative;
        overflow: hidden;
        margin-bottom: 1rem;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    /* Info Cards */
    .info-card {
        background: linear-gradient(to right, #FFFFFF, #F8FAFC);
        border-radius: 12px;
        padding: 24px 28px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
        margin-bottom: 2.5rem;
        color: #334155;
        font-size: 1.05rem;
        font-weight: 500;
    }

    /* Modern Pill Tabs */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 10px;
        background: #F1F5F9;
        padding: 8px;
        border-radius: 16px;
        border-bottom: none;
        margin-bottom: 3rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 12px 28px;
        color: #64748B;
        font-weight: 600;
        font-size: 1.05rem;
        border: none !important;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #0F172A;
        background: rgba(255, 255, 255, 0.5);
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03) !important;
        border: none !important;
    }

    /* Typography */
    h2, h3 {
        color: #1E293B !important;
        font-weight: 700 !important;
    }

    /* Dataframes soft shadow */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }

    /* Custom Divider */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #E2E8F0, transparent);
        margin: 3rem 0;
    }
</style>
"""
st.markdown(css_premium, unsafe_allow_html=True)

st.markdown("<h1 class='premium-title'>Sistem Pendukung Keputusan Pemilihan Laptop</h1>", unsafe_allow_html=True)
st.markdown("<p class='premium-subtitle'>Analisis Komparatif Multi-Criteria Decision Making (SAW, TOPSIS, WASPAS)</p>", unsafe_allow_html=True)

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

st.sidebar.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Parameter Analisis</h3>", unsafe_allow_html=True)
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

# Perhitungan SAW
matriks_normalisasi_saw = np.zeros_like(matriks_keputusan, dtype=float)
for kolom in range(jumlah_kolom):
    data_kolom = matriks_keputusan[:, kolom]
    if status_kriteria[kolom] == 'benefit':
        matriks_normalisasi_saw[:, kolom] = data_kolom / np.max(data_kolom)
    else:
        matriks_normalisasi_saw[:, kolom] = np.min(data_kolom) / data_kolom
nilai_akhir_saw = np.sum(matriks_normalisasi_saw * bobot_kriteria, axis=1)

# Perhitungan TOPSIS
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

# Perhitungan WASPAS
nilai_wsm = np.sum(matriks_normalisasi_saw * bobot_kriteria, axis=1)
nilai_wpm = np.prod(matriks_normalisasi_saw ** bobot_kriteria, axis=1)
konstanta_lambda = 0.5
nilai_akhir_waspas = (konstanta_lambda * nilai_wsm) + ((1 - konstanta_lambda) * nilai_wpm)

tab_dashboard, tab_saw, tab_topsis, tab_waspas, tab_visual = st.tabs([
    "Dashboard Eksekutif",
    "Analisis Algoritma SAW",
    "Analisis Algoritma TOPSIS",
    "Analisis Algoritma WASPAS",
    "Distribusi Pemeringkatan"
])

with tab_dashboard:
    st.markdown("<div class='info-card'>Menampilkan spesifikasi teknis kandidat komputasi portabel berdasarkan optimasi parameter *budgeting* dan memori. Dataset tersaring ini menginisiasi komputasi Matriks Keputusan Dasar (X).</div>", unsafe_allow_html=True)
    st.dataframe(dataframe_laptop, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 2.5rem; font-size: 2rem;'>Laporan Perbandingan Peringkat Akhir</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><h3 style='color: #0F172A; font-size: 1.4rem; margin-bottom: 1.5rem;'>Skoring Metode SAW</h3></div>", unsafe_allow_html=True)
        df_saw = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor Evaluasi': nilai_akhir_saw}).sort_values('Skor Evaluasi', ascending=False).reset_index(drop=True)
        df_saw.index = df_saw.index + 1
        st.dataframe(df_saw, use_container_width=True)
    with col2:
        st.markdown("<div class='metric-card'><h3 style='color: #0F172A; font-size: 1.4rem; margin-bottom: 1.5rem;'>Skoring Metode TOPSIS</h3></div>", unsafe_allow_html=True)
        df_topsis = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor Evaluasi': kedekatan_relatif}).sort_values('Skor Evaluasi', ascending=False).reset_index(drop=True)
        df_topsis.index = df_topsis.index + 1
        st.dataframe(df_topsis, use_container_width=True)
    with col3:
        st.markdown("<div class='metric-card'><h3 style='color: #0F172A; font-size: 1.4rem; margin-bottom: 1.5rem;'>Skoring Metode WASPAS</h3></div>", unsafe_allow_html=True)
        df_waspas = pd.DataFrame({'Alternatif': nama_alternatif, 'Skor Evaluasi': nilai_akhir_waspas}).sort_values('Skor Evaluasi', ascending=False).reset_index(drop=True)
        df_waspas.index = df_waspas.index + 1
        st.dataframe(df_waspas, use_container_width=True)

with tab_saw:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Dekomposisi Simple Additive Weighting (SAW)</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-card'><b>Fase 1: Matriks Keputusan Ternormalisasi (R)</b><br>Menyeleraskan metrik data dengan mentransformasi seluruh variabel ke dalam skala desimal (0-1) berpatokan pada fungsi objektif masing-masing atribut.</div>", unsafe_allow_html=True)
    df_norm_saw = pd.DataFrame(matriks_normalisasi_saw, columns=nama_kriteria, index=nama_alternatif)
    st.dataframe(df_norm_saw, use_container_width=True)
    
    st.markdown("<br><div class='info-card'><b>Fase 2: Ekstraksi Nilai Preferensi Global (V)</b><br>Menjumlahkan seluruh metrik pasca-normalisasi secara aditif linear, yang telah diberi pembobotan signifikansi.</div>", unsafe_allow_html=True)
    df_hasil_saw = pd.DataFrame({'Nilai Preferensi': nilai_akhir_saw}, index=nama_alternatif).sort_values('Nilai Preferensi', ascending=False)
    st.dataframe(df_hasil_saw, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_topsis:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Dekomposisi Algoritma TOPSIS</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-card'><b>Fase 1: Matriks Proyeksi Terbobot (Y)</b><br>Normalisasi berbasis akar kuadrat yang terintegrasi secara langsung dengan vektor bobot sistem.</div>", unsafe_allow_html=True)
    df_norm_topsis = pd.DataFrame(matriks_terbobot_topsis, columns=nama_kriteria, index=nama_alternatif)
    st.dataframe(df_norm_topsis, use_container_width=True)
    
    st.markdown("<br><div class='info-card'><b>Fase 2: Penentuan Solusi Ideal Ekstrem</b><br>Kalkulasi titik referensi absolut (Sempurna dan Terburuk) pada setiap metrik evaluasi.</div>", unsafe_allow_html=True)
    df_ideal = pd.DataFrame([solusi_ideal_positif, solusi_ideal_negatif], columns=nama_kriteria, index=['Solusi Ideal Positif (A+)', 'Solusi Ideal Negatif (A-)'])
    st.dataframe(df_ideal, use_container_width=True)
    
    st.markdown("<br><div class='info-card'><b>Fase 3: Jarak Geometris dan Nilai Komparasi</b><br>Mengalkulasi Kedekatan Relatif Euclidean untuk menentukan alternatif yang memiliki deviasi terkecil terhadap solusi sempurna.</div>", unsafe_allow_html=True)
    df_hasil_topsis = pd.DataFrame({'Jarak Sempurna (D+)': jarak_positif, 'Jarak Terburuk (D-)': jarak_negatif, 'Kedekatan Relatif': kedekatan_relatif}, index=nama_alternatif).sort_values('Kedekatan Relatif', ascending=False)
    st.dataframe(df_hasil_topsis, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_waspas:
    st.markdown("<div style='padding: 1rem 3rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Dekomposisi Algoritma WASPAS</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-card'><b>Fase 1: Evaluasi Dual-Model (WSM & WPM)</b><br>Mengisolasi hasil kalkulasi dari dua pendekatan matematis ekstrem: aditif dan eksponensial secara independen.</div>", unsafe_allow_html=True)
    df_wsm_wpm = pd.DataFrame({'Skor WSM (Aditif)': nilai_wsm, 'Skor WPM (Eksponensial)': nilai_wpm}, index=nama_alternatif)
    st.dataframe(df_wsm_wpm, use_container_width=True)
    
    st.markdown(f"<br><div class='info-card'><b>Fase 2: Asimilasi Hibrida ($\lambda = {konstanta_lambda}$)</b><br>Melahirkan keputusan mutlak melalui agregasi keseimbangan parameter linear dan eksponensial.</div>", unsafe_allow_html=True)
    df_hasil_waspas = pd.DataFrame({'Skor Integritas Akhir (Q)': nilai_akhir_waspas}, index=nama_alternatif).sort_values('Skor Integritas Akhir (Q)', ascending=False)
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
        axis[index_ax].barh(label_urut[::-1], skor_urut[::-1], color=warna_urut[::-1], edgecolor='#1E293B', linewidth=0.5)
        axis[index_ax].set_title(f'Peringkat {nama_metode}', fontsize=14, fontweight='bold', color='#0F172A', pad=15)
        axis[index_ax].set_xlabel('Nilai Evaluasi', fontsize=11, color='#475569')
        axis[index_ax].tick_params(axis='y', labelsize=10, colors='#1E293B')
        axis[index_ax].tick_params(axis='x', colors='#64748B')
        axis[index_ax].grid(axis='x', linestyle='--', alpha=0.3)
        axis[index_ax].spines['top'].set_visible(False)
        axis[index_ax].spines['right'].set_visible(False)
        axis[index_ax].spines['left'].set_color('#CBD5E1')
        axis[index_ax].spines['bottom'].set_color('#CBD5E1')
        for idx_bar, v_bar in enumerate(skor_urut[::-1]):
            axis[index_ax].text(v_bar + (0.01 * np.max(skor_urut)), idx_bar, f'{v_bar:.4f}', va='center', fontsize=9, color='#0F172A', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
