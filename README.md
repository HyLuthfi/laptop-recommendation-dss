<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3b82f6,100:0f172a&height=120&section=header" width="100%">

<div align="center">
  <br />
  <br />

# 💻 LAPTOP RECOMMENDATION DSS

<a href="https://github.com/HyLuthfi"><img src="https://readme-typing-svg.demolab.com?font=Outfit&weight=800&size=22&pause=1000&color=3B82F6&center=true&vCenter=true&width=800&lines=Automated+Decision+Support+System;Multi-Criteria+Decision+Making+(MCDM);SAW,+TOPSIS,+and+WASPAS+Algorithms;Data-Driven+Laptop+Recommendations" alt="Typing SVG" /></a>

  <br />
  <a href="https://laptop-recommendation-dss.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/_LAUNCH_LIVE_APP-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo Streamlit">
  </a>
  <br />
  <br />

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
    <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  </p>

  <p align="center">
    Sistem Pendukung Keputusan (DSS) cerdas berbasis Python dan Streamlit untuk memberikan rekomendasi laptop terbaik secara objektif. Menggunakan algoritma <b>SAW, TOPSIS, dan WASPAS</b> dengan antarmuka analitik <i>Premium Dashboard</i>.
  </p>
</div>

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## ✨ Fitur Utama

<table align="center" width="100%">
  <tr>
    <td width="50%" valign="top">
      <b>Data-Driven Filtering</b><br/>
      Memfilter 1,300+ dataset laptop asli berdasarkan <i>budget constraints</i> dan kebutuhan RAM minimum pengguna secara dinamis.
    </td>
    <td width="50%" valign="top">
      <b>Multi-Algorithm Analytics</b><br/>
      Komparasi <i>real-time</i> menggunakan 3 algoritma MCDM terkemuka (SAW, TOPSIS, dan WASPAS) untuk meminimalkan bias merek (<i>brand bias</i>).
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>Executive Dashboard</b><br/>
      Antarmuka Web Streamlit dengan desain <i>Premium Glassmorphism</i> yang responsif dan interaktif.
    </td>
    <td width="50%" valign="top">
      <b>Decomposition Transparency</b><br/>
      Menampilkan seluruh langkah perhitungan matematis secara rinci (Fase Normalisasi hingga Preferensi) pada setiap tab algoritma.
    </td>
  </tr>
</table>

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## 🧮 Arsitektur Algoritma & Kriteria

Sistem mengevaluasi setiap laptop berdasarkan matriks keputusan komprehensif:

**Bobot Kriteria (Criteria Weights):**

- **C1 (Harga/Price)** - 35% Bobot `(Atribut Cost)`
- **C2 (Kapasitas RAM)** - 20% Bobot `(Atribut Benefit)`
- **C3 (Kapasitas Storage)** - 20% Bobot `(Atribut Benefit)`
- **C4 (Berat/Weight)** - 15% Bobot `(Atribut Cost)`
- **C5 (Ukuran Layar/Screen)** - 10% Bobot `(Atribut Benefit)`

**Implementasi Algoritma:**

1. **SAW (Simple Additive Weighting):** Metode penjumlahan terbobot klasik.
2. **TOPSIS:** Mengevaluasi metrik berdasarkan jarak terpendek ke solusi ideal positif (A+) dan terjauh dari ideal negatif (A-).
3. **WASPAS:** Kombinasi <i>hybrid</i> aditif dan eksponensial (WSM & WPM) dengan parameter agregasi λ = 0.5.

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## 🚀 Panduan Instalasi & Eksekusi

Sistem ini bisa dijalankan melalui Jupyter Notebook atau sebagai Web Aplikasi Streamlit.

### Opsi 1: Menjalankan Streamlit Web App

1. **Clone Repository**
   ```bash
   git clone https://github.com/HyLuthfi/laptop-recommendation-dss.git
   cd laptop-recommendation-dss
   ```
2. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Server Streamlit**
   ```bash
   streamlit run app.py
   ```

### Opsi 2: Eksekusi via Jupyter Notebook

Buka file `pemilihan_laptop.ipynb` untuk melihat eksekusi algoritma baris-demi-baris, normalisasi data <i>raw</i>, dan visualisasi bar chart menggunakan <i>Matplotlib</i>.

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:3b82f6,100:0f172a&height=120&section=footer" width="100%"/>
</p>
