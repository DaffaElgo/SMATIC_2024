# Simulasi Penyeberangan Kendaraan  
**🏆 Juara 1 Olimpiade Statistika “Smart Statistics (SMATIC) UNJ 2024”**

**Penulis**  
Team Estetic

**Repo:** https://github.com/DaffaElgo/SMATIC_2024

---

## Deskripsi Proyek  
Repository ini memuat implementasi simulasi penyeberangan pejalan kaki berdasarkan data selang waktu antar kendaraan. Metode yang digunakan adalah **Simulasi Monte Carlo** untuk menentukan durasi lampu merah penyeberangan (parameter _L_) agar efisiensi keamanan pejalan kaki dan kelancaran arus lalu lintas optimal.

## Latar Belakang  
Pada banyak lokasi penyeberangan tanpa lampu lalu lintas, selang waktu kendaraan yang terlalu singkat atau terlalu panjang dapat mengancam keselamatan pejalan kaki maupun menyebabkan kemacetan. Model variabel acak dan simulasi Monte Carlo memungkinkan rekomendasi durasi lampu merah yang data-driven.

## Prestasi  
> **🏅 Juara 1 Olimpiade Statistika SMATIC UNJ 2024**  
> — Kompetisi “Smart Statistics Competition”  
> — Babak Final: Analisis data selang waktu kendaraan, simulasi, dan rekomendasi kebijakan  

## Fitur Utama  
- **Pembacaan data** dari file Excel (.xlsx)  
- **Simulasi Monte Carlo** dengan distribusi Poisson untuk kedatangan pejalan kaki  
- **Evaluasi efisiensi**: rasio pejalan kaki yang menyeberang sukses vs. total antrean  
- **Output**: Tabel Optimal _L_, Tabel Alternatif _L_, dan visualisasi (2D & 3D)  
- **GUI interaktif** berbasis Tkinter untuk input parameter dan tampilan hasil  
