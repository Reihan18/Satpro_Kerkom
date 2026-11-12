# Ruang Nilai — Student Academic Performance

Dashboard interaktif untuk tugas Statistika dan Probabilitas 1 menggunakan Python, Streamlit, Pandas, dan Plotly.

## Dataset
- **Nama:** Students Performance in Exams
- **Sumber:** https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
- **File:** `data/data.csv`
- **Isi:** 1.000 baris, 8 kolom, terdiri dari 3 kolom nilai numerik dan 5 kolom kategori.
- Dataset sumber tidak memiliki tanggal/waktu. Data tanggal tidak dibuat-buat; analisis difokuskan pada perbandingan dan hubungan antarvariabel.

## Pertanyaan analisis
1. Apakah persiapan ujian berkaitan dengan nilai siswa?
2. Bagaimana hubungan nilai matematika, membaca, dan menulis?
3. Apakah kelompok siswa memiliki sebaran nilai berbeda berdasarkan gender dan kategori makan siang?

## Fitur dashboard
- Filter interaktif untuk gender, persiapan ujian, dan kategori makan siang.
- Kartu ringkasan jumlah siswa, rata-rata, median, dan nilai rata-rata tertinggi.
- Grafik perbandingan nilai berdasarkan persiapan ujian.
- Matriks korelasi dan scatter plot dengan pilihan variabel.
- Boxplot perbandingan kelompok siswa.
- Statistik deskriptif (mean, median, standar deviasi, kuartil, dan IQR).
- Histogram dan deteksi outlier menggunakan metode IQR.
- Informasi pemeriksaan missing value dan duplikat.

## Instalasi dan menjalankan
Buka terminal pada folder project, lalu jalankan:

```bash
python -m pip install -r requirements.txt
python -m streamlit run dashboard.py
```

## Struktur folder
```text
Student_Performance_Green_Dashboard/
├── dashboard.py
├── requirements.txt
├── README.md
└── data/
    └── data.csv
```

## Catatan
Analisis bersifat deskriptif. Perbedaan dan korelasi yang ditemukan tidak dapat langsung diartikan sebagai hubungan sebab-akibat.


## Tema tampilan
Dashboard menggunakan tema hijau, putih, dan abu-abu muda. CSS multiselect juga telah ditulis ulang dengan selector khusus `stMultiSelect` dan BaseWeb untuk mengatur latar kotak, chip pilihan, ikon, serta menu dropdown.


## Pembaruan keterbacaan grafik
Seluruh konfigurasi grafik Plotly menggunakan latar putih dan warna teks kontras tinggi:
judul abu-abu gelap, label/sumbu hijau keabu-abuan gelap, serta angka heatmap putih.
CSS tambahan menjaga teks grafik tetap terbaca.


## Perbaikan kompatibilitas Plotly
Konfigurasi `plot_config` tidak lagi menyertakan argumen `title` bersama,
sehingga pemanggilan `update_layout(**plot_config, title=...)` tidak menghasilkan
TypeError akibat argumen `title` ganda. Warna teks sumbu, tick, legenda, dan colorbar
tetap menggunakan warna kontras tinggi.
