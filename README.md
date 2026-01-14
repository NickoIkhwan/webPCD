---
title: PCD
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🚦 Sistem Kontrol Lalu Lintas Pintar (Berbasis YOLO)

[![Buka di GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/NickoIkhwan/webPCD)

Aplikasi web berbasis Django modern yang menggunakan **YOLO (You Only Look Once)** untuk mendeteksi kendaraan secara real-time dan mengontrol lampu lalu lintas secara cerdas berdasarkan kepadatan kendaraan.

## 🚀 Fitur Utama
- **Deteksi Kendaraan Real-time**: Menggunakan YOLO (Ultralytics) untuk klasifikasi kendaraan dengan akurasi tinggi.
- **Logika Lalu Lintas Pintar**: Timer lampu lalu lintas dinamis berdasarkan "Bobot Lalu Lintas" (Kendaraan besar = bobot lebih tinggi).
- **Dashboard Interaktif**: UI modern dengan streaming pemrosesan video/kamera secara langsung.
- **Dukungan File**: Memproses file gambar statis maupun video.
- **Optimasi CPU**: Dikonfigurasi untuk berjalan efisien pada server/laptop standar tanpa GPU khusus.

## 🛠️ Mulai Cepat

### 1. Pengujian Langsung (GitHub Codespaces)
Cara termudah bagi dosen untuk menguji proyek ini adalah melalui **GitHub Codespaces**:
1. Buka [Repositori GitHub](https://github.com/NickoIkhwan/webPCD).
2. Klik tombol hijau **Code** dan pilih **Codespaces**.
3. Buat codespace baru pada branch `main`.
4. Tunggu lingkungan dibangun (dependensi akan terinstal secara otomatis).
5. Buka terminal dan jalankan:
   ```bash
   python manage.py runserver
   ```
6. Klik **Open in Browser** saat notifikasi muncul.

### 2. Pengaturan Lokal
```bash
# Clone repositori
git clone https://github.com/NickoIkhwan/webPCD.git
cd webPCD

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate

# Instal dependensi
pip install -r requirements.txt

# Jalankan migrasi database
python manage.py migrate

# Jalankan server
python manage.py runserver
```

## 🏗️ Arsitektur Teknis
- **Backend**: Django (Python)
- **Computer Vision**: OpenCV, Ultralytics YOLOv8
- **Frontend**: Tailwind CSS, PostCSS
- **Model**: Model YOLO kustom yang terletak di `myapp/media/model_4/`

## 📄 Lisensi
Proyek ini dibuat untuk tujuan pendidikan sebagai Tugas Akhir mata kuliah Pengolahan Citra Digital (PCD).

---
