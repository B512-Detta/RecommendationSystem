# -*- coding: utf-8 -*-
"""RecommendationSystem-Cell

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PdmfUpwa9Rhuy1R1Y3NXCtB1h8v-4lr4

**Import Library**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

"""# **Data Understanding**

**Unzip Dataset**
"""

!unzip '/content/archive (2).zip'

"""**Data Loading**"""

ratings_df = pd.read_csv('cellphones ratings.csv')
users_df = pd.read_csv('cellphones users.csv')
cellphones_df = pd.read_csv('cellphones data.csv')

"""**Mengeluarkan output basic dari dari masing-masing data**"""

print("Ratings Data:")
print(ratings_df.info())
print(ratings_df.head())

print("\nUsers Data:")
print(users_df.info())
print(users_df.head())

print("\nCellphones Data:")
print(cellphones_df.info())
print(cellphones_df.head())

"""**Visualisasi Distribusi Rating**"""

sns.histplot(ratings_df['rating'], bins=10, kde=False, color='blue')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

"""**Visualisasi Distribusi Usia dan Gender Pengguna**"""

plt.figure(figsize=(10, 5))
sns.histplot(users_df['age'], bins=15, kde=True, color='green')
plt.title('Distribution of User Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

sns.countplot(data=users_df, x='gender', palette='Set2')
plt.title('Gender Distribution')
plt.show()

"""Informasi Data Ponsel"""

print("Unique Brands in Dataset:", cellphones_df['brand'].nunique())
print("Unique Models in Dataset:", cellphones_df['model'].nunique())
print(cellphones_df.describe(include='all'))

"""# **Data Preparation**

**Cek apakah ada data yang missing value**
"""

print("Missing values in Ratings Data:")
print(ratings_df.isnull().sum())

print("\nMissing values in Users Data:")
print(users_df.isnull().sum())

print("\nMissing values in Cellphones Data:")
print(cellphones_df.isnull().sum())

"""**terdapat missing value pada data 'User Data'**"""

users_df = users_df.dropna()

"""**Convert Date**

Mengubah kolom relase date yang berada di var 'cellphone_df' menjadi tipe datetime
"""

cellphones_df['release date'] = pd.to_datetime(cellphones_df['release date'], format='%d/%m/%Y')
scaler = MinMaxScaler()
numerical_cols = ['internal memory', 'RAM', 'performance', 'battery size',
                  'screen size', 'weight', 'price']
cellphones_df[numerical_cols] = scaler.fit_transform(cellphones_df[numerical_cols])
print(cellphones_df.head())

"""**Join Dataset**

Menggabungkan dataset 'ratings_df' dengan 'cellphones_df' berdasarkan cellphone_id, dan ratings_df dengan users_df berdasarkan user_id.
"""

merged_df = pd.merge(ratings_df, cellphones_df, on='cellphone_id', how='inner')
merged_df = pd.merge(merged_df, users_df, on='user_id', how='inner')
print("Merged Data:")
print(merged_df.info())
print(merged_df.head())

"""Visualisasi
1. Distribusi price setelah normalisasi.
2. Perbandingan rating terhadap brand.
"""

sns.histplot(cellphones_df['price'], kde=True, color='purple')
plt.title('Distribution of Normalized Prices')
plt.xlabel('Normalized Price')
plt.ylabel('Frequency')
plt.show()

sns.boxplot(data=merged_df, x='brand', y='rating', palette='Set3')
plt.title('Ratings Distribution per Brand')
plt.xticks(rotation=45)
plt.show()

"""# **Data Modelling and Result**

**Content-Based Filtering**
"""

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Select features for similarity
features = ['internal memory', 'RAM', 'performance', 'battery size',
            'screen size', 'weight', 'price']
content_matrix = cellphones_df[features]

# Compute similarity matrix
similarity_matrix = cosine_similarity(content_matrix)

# Create function for top-N recommendation
def recommend_content_based(cellphone_id, top_n=5):
    idx = cellphones_df[cellphones_df['cellphone_id'] == cellphone_id].index[0]
    similar_indices = similarity_matrix[idx].argsort()[::-1][1:top_n+1]
    recommendations = cellphones_df.iloc[similar_indices]
    return recommendations[['cellphone_id', 'brand', 'model', 'price']]

# Example: Recommend based on cellphone ID 0
print("Content-Based Recommendations:")
print(recommend_content_based(cellphone_id=0, top_n=5))

"""**Collaborative Filtering**"""

# Pivot ratings into matrix form
ratings_matrix = ratings_df.pivot(index='user_id', columns='cellphone_id', values='rating').fillna(0)

# Convert to NumPy array
ratings_matrix_array = ratings_matrix.to_numpy()

# Check the dimensions of the matrix
num_users, num_items = ratings_matrix_array.shape
print(f"Matrix dimensions: Users = {num_users}, Items = {num_items}")

# Ensure k is less than min(num_users, num_items)
k = min(num_users, num_items) - 1  # Ensure k is valid
print(f"Using k = {k} for SVD")

# Perform SVD
from scipy.sparse.linalg import svds
U, sigma, Vt = svds(ratings_matrix_array, k=k)
sigma = np.diag(sigma)

# Predict ratings
predicted_ratings = np.dot(np.dot(U, sigma), Vt)

# Convert back to DataFrame
predicted_ratings_df = pd.DataFrame(predicted_ratings, columns=ratings_matrix.columns, index=ratings_matrix.index)

print("SVD Decomposition Completed!")

def recommend_collaborative(user_id, top_n=5):
    # Index user
    user_idx = ratings_matrix.index.get_loc(user_id)

    # Prediksi rating user
    user_ratings = predicted_ratings[user_idx]

    # Ponsel yang sudah dirating oleh user
    rated_items = ratings_matrix.iloc[user_idx][ratings_matrix.iloc[user_idx] > 0].index

    # Filter ponsel yang belum dirating
    unrated_items = [i for i in ratings_matrix.columns if i not in rated_items]

    # Ambil prediksi rating untuk ponsel yang belum dirating
    recommendations = {item: user_ratings[ratings_matrix.columns.get_loc(item)] for item in unrated_items}

    # Sort ponsel berdasarkan prediksi rating
    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Buat DataFrame rekomendasi
    recommended_cellphones = cellphones_df[cellphones_df['cellphone_id'].isin([x[0] for x in sorted_recommendations])]
    recommended_cellphones['predicted_rating'] = [x[1] for x in sorted_recommendations]

    return recommended_cellphones[['cellphone_id', 'brand', 'model', 'price', 'predicted_rating']]

top_recommendations = recommend_collaborative(user_id=0, top_n=5)
print("Collaborative Filtering Recommendations:")
print(top_recommendations)

"""Menyajikan Ouput dari 2 metode berbeda"""

# Content-Based
content_recommendations = recommend_content_based(cellphone_id=0, top_n=5)

# Collaborative Filtering
collaborative_recommendations = recommend_collaborative(user_id=0, top_n=5)

# Display results
print("Content-Based Recommendations:\n", content_recommendations)
print("\nCollaborative Filtering Recommendations:\n", collaborative_recommendations)

"""# **Evaluation**

Evaluasi Collaborative Filtering (CF) yaitu dengan menghitung RMSE.
RMSE (Root Mean Square Error) digunakan untuk mengukur seberapa akurat prediksi rating dibandingkan dengan rating sebenarnya.
"""

from sklearn.metrics import mean_squared_error
from math import sqrt

# Flatten predictions and actual ratings
actual_ratings = ratings_matrix.to_numpy().flatten()
predicted_ratings_flat = predicted_ratings.flatten()

# Filter out zero ratings (unrated items)
mask = actual_ratings > 0  # Hanya rating yang diberikan pengguna
rmse = sqrt(mean_squared_error(actual_ratings[mask], predicted_ratings_flat[mask]))

print(f"RMSE (Collaborative Filtering): {rmse}")

"""Evaluasi Content-Based Filtering (CBF) dengan menghitung Precision@N dan Recall@N.
Precision@N menghitung proporsi rekomendasi yang relevan, sedangkan Recall@N menghitung proporsi item relevan yang ditemukan dalam rekomendasi.
"""

def precision_recall_at_n(recommendations, relevant_items, n):
    top_n_recommendations = recommendations[:n]
    relevant_in_recommendations = set(top_n_recommendations).intersection(set(relevant_items))

    precision = len(relevant_in_recommendations) / n
    recall = len(relevant_in_recommendations) / len(relevant_items)
    return precision, recall

# Contoh data pengguna
user_id = 0

# Ambil ponsel yang sudah dirating oleh pengguna
rated_items = ratings_df[ratings_df['user_id'] == user_id]['cellphone_id'].tolist()

# Ambil rekomendasi CBF untuk user_id tertentu
cbf_recommendations = content_recommendations['cellphone_id'].tolist()

# Precision@5 dan Recall@5
precision, recall = precision_recall_at_n(cbf_recommendations, rated_items, n=5)
print(f"Precision@5: {precision}")
print(f"Recall@5: {recall}")

"""Analisis Hasil
1. Collaborative Filtering (CF):
RMSE yang rendah menunjukkan pendekatan ini cukup baik dalam memprediksi rating.
CF bergantung pada interaksi pengguna dengan produk. Jika ada lebih banyak data rating, model ini dapat lebih optimal.

2. Content-Based Filtering (CBF):
Precision lebih tinggi daripada Recall, yang mengindikasikan model dapat memberikan rekomendasi yang relevan, tetapi kurang mencakup semua item relevan.
Model ini hanya mempertimbangkan kesamaan fitur ponsel, sehingga rekomendasi lebih terbatas pada kemiripan karakteristik dibandingkan preferensi pengguna.

"""

