# CCTV AI Pipeline - Real-time Detection & Tracking

Proyek ini adalah implementasi pipeline AI untuk memproses stream video, melakukan deteksi objek (orang), dan melacak pergerakan setiap individu dengan ID yang stabil.

## Arsitektur Pipeline

Pipeline ini dibangun dengan arsitektur Python yang modular untuk memastikan kode mudah dikelola dan dikembangkan.

- **`app.py`**: Antarmuka pengguna berbasis Streamlit.
- **`src/`**: Berisi semua logika inti:
  - `video_stream.py`: Class untuk mengelola koneksi ke sumber video (termasuk RTSP) dan menangani proses `reconnect` otomatis.
  - `detector.py`: Class wrapper untuk model deteksi dan tracking (YOLOv8 + ByteTrack).
  - `config.py`: File konfigurasi terpusat.

Alur data: `VideoStream` -> `Detector` -> `Streamlit UI`

## Strategi Real-time Optimization

Untuk mencapai performa yang mendekati real-time, strategi **Frame Skipping** diterapkan.

- Mekanisme: Pipeline tidak memproses setiap frame dari video. Pengaturan `FRAME_SKIP` di `config.py` menentukan bahwa hanya 1 dari setiap N frame yang akan dimasukkan ke model AI.
- Tujuan: Mengurangi beban komputasi secara signifikan, sehingga meningkatkan FPS tanpa kehilangan kemampuan tracking secara drastis, karena objek tidak bergerak terlalu jauh dalam beberapa frame.

## Penanganan Error Jaringan (Reconnect Otomatis)

Ketangguhan sistem adalah prioritas. Class `VideoStream` dirancang untuk menangani koneksi yang tidak stabil.

- Jika stream terputus (`cap.read()` gagal), pipeline tidak akan crash.
- Sistem akan menunggu selama `RECONNECT_DELAY_SECONDS` (dapat dikonfigurasi) sebelum secara otomatis mencoba untuk membangun kembali koneksi ke stream video.
- Selama proses ini, dashboard akan menampilkan status peringatan kepada pengguna.

## Cara Menjalankan

1.  Pastikan Python 3.8+ terinstal.
2.  Buat dan aktifkan virtual environment.
3.  Install semua dependensi:
    ```bash
    pip install -r requirements.txt
    ```
4.  Jalankan aplikasi Streamlit:
    ```bash
    streamlit run app.py
    ```
