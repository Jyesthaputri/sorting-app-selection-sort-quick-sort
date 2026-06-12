# Cara kerja:
    # - load_xlsx() membaca file Excel dan mengekstrak kolom 'Keaktifan' sebagai
    #   list angka yang siap diproses oleh algoritma sorting
    # - save_xlsx() menyimpan kembali hasil sorting ke file Excel baru
    #   tanpa mengubah file asli
# Struktur file Excel yang didukung:
    # Baris 1 : Judul tabel (dilewati, bukan header)
    # Baris 2 : Header kolom → No | Nama Siswa | Keaktifan  ← header=1
    # Baris 3+: Data siswa

import pandas as pd     # Library untuk membaca dan memanipulasi data tabular (Excel, CSV, dll)

def load_xlsx(path):    # Baca file Excel dengan openpyxl sebagai engine
    df = pd.read_excel(path, engine='openpyxl', header=1)  # header=1 → baris index ke-1 (baris ke-2 di Excel) dipakai sebagai header kolom
    
    # ── Tampilkan informasi file ke terminal untuk membantu debugging ───────────
    print("Kolom tersedia:", df.columns.tolist())   # Cek nama kolom yang terbaca
    print("Total data:", len(df))                   # Cek jumlah baris data
    print("Preview:\n", df.head())                  # Cek jumlah baris data
    
    data = df['Keaktifan'].tolist()     # Ekstrak kolom 'Keaktifan' sebagai list angka
    
    return data, df     # Kembalikan list data dan DataFrame lengkap

def save_xlsx(df, sorted_data, path):
    df_output = df.copy()       # Salin DataFrame agar data asli tidak ikut berubah
    df_output['Keaktifan'] = sorted_data    # Ganti kolom 'Keaktifan' dengan data yang sudah terurut (descending)
    df_output.to_excel(path, index=False, engine='openpyxl')    # Simpan ke file Excel baru
    print(f"File berhasil disimpan ke: {path}")     # Konfirmasi penyimpanan ke terminal