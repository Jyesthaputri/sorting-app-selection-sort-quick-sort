# Cara kerja:
    # - Setiap iterasi mencari nilai TERBESAR dari sisa array yang belum terurut
    # - Nilai terbesar tersebut ditukar ke posisi paling depan (index i)
    # - Proses diulang sampai seluruh array terurut
# Kompleksitas Waktu : O(n²) — untuk semua kasus (best, average, worst)
# Kompleksitas Ruang : O(1)  — in-place, tidak butuh array tambahan
# Jumlah Swap        : Minimal (maksimal n-1 swap), efisien dalam hal swap

import time     # Digunakan untuk mengukur waktu eksekusi secara akurat

def selection_sort(data): #Mengurutkan data dari nilai tertinggi ke terendah (descending) menggunakan algoritma Selection Sort.
    arr = data.copy()       # Salin data agar data asli tidak berubah
    n = len(arr)            # Jumlah elemen dalam array
    swaps = 0               # Penghitung jumlah pertukaran (swap) yang terjadi
    comparisons = 0         # Penghitung jumlah perbandingan (comparison) yang terjadi

    start = time.perf_counter()     # Mulai pencatatan waktu eksekusi
    # perf_counter() lebih akurat dari time() untuk pengukuran durasi pendek

# ── Loop Utama ────────────────────────────────────────────────────────────
# Setiap iterasi i menempatkan elemen terbesar ke posisi i
# Setelah iterasi ke-i, posisi 0..i sudah terurut dengan benar
    for i in range(n):
        max_idx = i  # Index elemen terbesar yang ditemukan sejauh ini (Asumsikan elemen di posisi i adalah yang terbesar sementara ini)

# ── Loop Pencarian Nilai Terbesar ──────────────────────────────────────
        # Cari elemen terbesar dari sisa array yang belum terurut (i+1 hingga akhir)
        for j in range(i + 1, n):
            comparisons += 1            # Hitung setiap perbandingan yang terjadi
            if arr[j] > arr[max_idx]:   # Jika elemen j lebih besar dari max saat ini
                max_idx = j             # Perbarui index elemen terbesar

# ── Pertukaran (Swap) ──────────────────────────────────────────────────
        # Tukar elemen terbesar ke posisi i, HANYA jika posisinya memang berbeda
        # Inilah mengapa Selection Sort sangat hemat swap (maks n-1 swap)
        if max_idx != i:
            arr[i], arr[max_idx] = arr[max_idx], arr[i]
            swaps += 1              # Hitung pertukaran yang terjadi

    elapsed = (time.perf_counter() - start) * 1000  # Hitung total waktu eksekusi dan konversi dari detik ke milidetik

    return {      # Kembalikan hasil dalam format dict yang konsisten dengan algoritma lainnya
        'name': 'Selection Sort',      
        'sorted': arr,                  
        'swaps': swaps,                 
        'comparisons': comparisons,     
        'time': round(elapsed, 2)       
    }