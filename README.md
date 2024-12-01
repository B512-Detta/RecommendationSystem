# Laporan Proyek Machine Learning - Bernadetta Sri Endah Dwi

## Project Overview

Dalam era digital saat ini, kebutuhan konsumen terhadap perangkat elektronik, terutama smartphone, semakin meningkat. Salah satu cara untuk memenuhi kebutuhan ini adalah dengan menyediakan rekomendasi yang relevan berdasarkan preferensi pengguna. Proyek ini bertujuan untuk membangun sistem rekomendasi smartphone menggunakan dua pendekatan populer dalam sistem rekomendasi: Content-Based Filtering dan Collaborative Filtering.

Proyek ini penting karena dapat membantu pengguna untuk menemukan smartphone yang sesuai dengan preferensi mereka dengan lebih cepat dan efisien. Selain itu, sistem rekomendasi dapat meningkatkan pengalaman pengguna dan meningkatkan penjualan produk bagi perusahaan yang mengadopsi teknologi ini.

## Business Understanding
### Problem Statements
1. Bagaimana cara memberikan rekomendasi smartphone yang relevan kepada pengguna berdasarkan preferensi mereka?
2. Apa pendekatan yang dapat digunakan untuk meningkatkan akurasi sistem rekomendasi pada dataset yang terbatas?

### Goals
1. Mengembangkan sistem rekomendasi yang dapat memberikan rekomendasi smartphone berdasarkan rating dan fitur produk.
2. Menggunakan dua metode berbeda, yaitu Content-Based Filtering dan Collaborative Filtering, untuk mengevaluasi efektivitas keduanya dalam memberikan rekomendasi yang akurat.

### Solution Approach
1. Content-Based Filtering: Menggunakan fitur produk (misalnya harga, brand, RAM, dan lainnya) untuk memberikan rekomendasi berdasarkan kesamaan antara produk yang disukai pengguna dengan produk lainnya.
2. Collaborative Filtering: Menggunakan data rating pengguna untuk memprediksi rating yang belum diberikan oleh pengguna pada produk tertentu, kemudian merekomendasikan produk dengan rating tertinggi.

## Data Understanding
### Dataset
| Jenis              | Keterangan                    |
|--------------------|-------------------------------|
| Title              | Cellphones Recommendations  |
| Source             | https://www.kaggle.com/datasets/meirnizri/cellphones-recommendations|
| License            | https://opendatacommons.org/licenses/odbl/1-0/|
| Visibility         | Public                        |
| Tags               | Pre-trained model, Electronic, E-Commerce Service, Mobile and Wireless, Recommender System|
| Usability          | 10.00                          |

### Dataset yang digunakan dalam proyek ini terdiri dari tiga file CSV:
cellphone_ratings.csv: Berisi data rating yang diberikan pengguna terhadap smartphone.
cellphone_user.csv: Berisi data pengguna, termasuk usia, jenis kelamin, dan pekerjaan.
cellphonedata.csv: Berisi informasi fitur terkait smartphone seperti brand, model, harga, RAM, dan lainnya.

### Jumlah data:
cellphone_ratings.csv: 99 pengguna, 33 produk.
cellphone_user.csv: 99 pengguna.
cellphonedata.csv: 33 smartphone.

### Variabel pada Dataset
cellphone_ratings.csv:
user_id: ID pengguna.
cellphone_id: ID smartphone.
rating: Rating yang diberikan oleh pengguna untuk smartphone.

cellphone_user.csv:
user_id: ID pengguna.
age: Usia pengguna.
gender: Jenis kelamin pengguna.
occupation: Pekerjaan pengguna.

cellphonedata.csv:
cellphone_id: ID smartphone.
brand: Merk smartphone.
model: Model smartphone.
price: Harga smartphone.
RAM, internal memory, performance, dll.

### Visualisasi Distribus Rating
Distribusi rating pengguna terhadap smartphone memberikan gambaran sebaran penilaian yang diberikan oleh pengguna. Berikut adalah grafik distribusi rating:

![image](https://github.com/user-attachments/assets/1c8db077-63e7-4914-a266-44d19a4c837a)

### Visualisasi Distribusi Usia dan Gender Pengguna
Distribusi usia dan gender pengguna memberikan wawasan tentang karakteristik demografis pengguna yang memberikan rating terhadap produk. Berikut adalah grafik distribusi usia dan gender pengguna:

![image](https://github.com/user-attachments/assets/680dec53-f57b-4229-bb20-6ccf61db019f)
![image](https://github.com/user-attachments/assets/6c1c8f1f-bfe1-4163-89a6-62160f2a36a8)


## Data Preparation
Pada tahap ini, data dibersihkan dan dipersiapkan untuk analisis lebih lanjut. Tahapan yang dilakukan:
- Menghapus Missing Values: Kolom yang memiliki nilai hilang (missing) dihapus dari dataset, dan terdapat missing value pada data pengguna/User data tepatnya pada kolom occupation.
- Mengonversi Tipe Data: Kolom yang tidak sesuai tipe data dikonversi, seperti mengonversi release date menjadi format tanggal.
- Membuat Matriks Rating: Data rating pengguna dikonversi menjadi matriks dengan pengguna sebagai baris dan smartphone sebagai kolom.

## Modeling
1. Content-Based Filtering
Menggunakan kesamaan fitur smartphone, seperti harga, RAM, dan lainnya, untuk memberikan rekomendasi produk yang serupa dengan yang telah dinilai oleh pengguna.
Output Content-Based Recommendations:

| No  | Cellphone ID | Brand  | Model                    | Price       |
|-----|--------------|--------|--------------------------|-------------|
| 1   | 1            | Apple  | iPhone 13 Mini           | 0.304976    |
| 2   | 2            | Apple  | iPhone 13                | 0.304976    |
| 3   | 3            | Apple  | iPhone 13 Pro            | 0.465490    |
| 4   | 10           | Samsung| Galaxy S22               | 0.213483    |
| 5   | 21           | OnePlus| 10T                      | 0.278224    |

2. Collaborative Filtering
Menggunakan data rating untuk memprediksi rating yang belum diberikan oleh pengguna dan memberikan rekomendasi berdasarkan prediksi tersebut.
Output Collaborative Filtering :
| No  | Cellphone ID | Brand   | Model                    | Price  | Predicted Rating |
|-----|--------------|---------|--------------------------|--------|------------------|
| 1   | 0            | Apple   | iPhone SE (2022)         | 429    | 0.149560         |
| 2   | 6            | Asus    | Zenfone 8                | 699    | 0.142755         |
| 3   | 11           | Samsung | Galaxy S22 Plus          | 999    | 0.140686         |
| 4   | 28           | Sony    | Xperia Pro               | 1199   | 0.090420         |
| 5   | 31           | Motorola| Moto G Pure              | 199    | 0.090374         |

## Evaluation
### Collaborative Filtering (CF)
- RMSE (Root Mean Square Error): 0.2949
Nilai RMSE yang rendah menunjukkan bahwa model Collaborative Filtering dapat memprediksi rating dengan cukup baik, meskipun masih ada ruang untuk perbaikan.
### Content-Based Filtering (CBF)
- Precision@5: 0.4
Dari 5 rekomendasi teratas, 40% merupakan item relevan.
- Recall@5: 0.2
Hanya 20% item relevan yang ditemukan dalam rekomendasi teratas.

### Kesimpulan
Collaborative Filtering lebih efektif dalam memprediksi rating produk meskipun membutuhkan lebih banyak data untuk meningkatkan akurasi.
Content-Based Filtering dapat memberikan rekomendasi yang relevan berdasarkan fitur produk, tetapi perlu perbaikan dalam mencakup lebih banyak produk relevan dalam rekomendasi.

### Saran
Untuk Collaborative Filtering, lebih banyak data pengguna dan rating akan membantu meningkatkan akurasi model.
Untuk Content-Based Filtering, dapat diperbaiki dengan menggunakan bobot fitur yang lebih tepat dan menggabungkan dengan teknik lain seperti hybrid filtering.

### Referensi 
1. Sarwar, Badrul, et al. "Item-based collaborative filtering recommendation algorithms." Proceedings of the 10th international conference on World Wide Web. 2000.
2. Kaggle. (2022). Cellphones Recommendations. Retrieved from https://www.kaggle.com/datasets/meirnizri/cellphones-recommendations
