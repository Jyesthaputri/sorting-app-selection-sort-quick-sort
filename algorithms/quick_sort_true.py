# Cara kerja:
    # - Pilih pivot menggunakan teknik Median Sejati (nilai tengah sesungguhnya dari sub-array yang sedang diproses setelah diurutkan sementara)
    # - Partisi array: elemen >= pivot ke kiri, elemen < pivot ke kanan
    # - Rekursif urutkan bagian kiri dan kanan dari pivot
# Perbandingan dengan varian Quick Sort lainnya:
    # - Pivot Pertama   → sederhana, sama rentannya dengan Pivot Terakhir terhadap worst case jika data sudah terurut
    # - Pivot Terakhir  → sama persis, hanya beda posisi pivot awal
    # - Median of Three → pivot dari 3 kandidat, lebih stabil
    # - Median Sejati   → pivot nilai tengah sesungguhnya, paling seimbang
# Kompleksitas Waktu : O(n log n) rata-rata, lebih stabil dari pivot acak
# Kompleksitas Ruang : O(n) — karena membuat sub-array sementara tiap partisi

import time         # Digunakan untuk mengukur waktu eksekusi secara akurat

swaps_count = 0         # Variabel global untuk melacak jumlah swap dan comparison lintas rekursi
comparisons_count = 0   # Direset ke 0 setiap kali quick_sort() dipanggil dari awal

# ── Median Sejati ───────────────────────────────────────────────────
# nilai median sesungguhnya dari sub-array arr[low..high] lalu menempatkannya di posisi arr[high] sebagai pivot untuk partition()
def median_sejati(arr, low, high):
    global swaps_count

    # Langkah 1: Salin sub-array ke list sementara,
    sub = arr[low:high + 1] # sub berisi salinan elemen arr[low] sampai arr[high]
    # Langkah 2: Urutkan sementara untuk menemukan nilai tengah
    sub_sorted = sorted(sub) #sorted() menggunakan Timsort bawaan Python (O(n log n)), Hasilnya ascending, indeks tengah = len//2
     # Langkah 3: Ambil nilai median dari posisi tengah
    median_val = sub_sorted[len(sub_sorted) // 2] # Untuk jumlah elemen genap: ambil elemen tengah bawah

    # Langkah 4: Cari index dengan median_val pada median di array asli, tukar ke posisi high
    for k in range(low, high + 1):
        if arr[k] == median_val:
            arr[k], arr[high] = arr[high], arr[k]   # Pindahkan median ke arr[high]
            swaps_count += 1                        # Hitung swap ini
            break                                   # Hentikan setelah median pertama ditemukan

# ── DIUBAH: partition pakai median sejati ────────────────────────────────────
def partition(arr, low, high):
    global swaps_count, comparisons_count

    # Tentukan pivot dengan median sejati sebelum partisi
    if high > low:                      #Terapkan Median Sejati hanya jika ada lebih dari 1 elemen
        median_sejati(arr, low, high)   # (jika hanya 1 elemen, tidak perlu mencari median)

    pivot = arr[high]    # Gunakan arr[high] sebagai pivot (sudah diisi nilai median oleh median_sejati() di atas)
    i = low - 1     # i adalah batas antara elemen >= pivot (kiri) dan < pivot (kanan), Dimulai dari low-1 karena belum ada elemen yang diproses

 # ── Loop Partisi ──────────────────────────────────────────────────────────
    for j in range(low, high):
        comparisons_count += 1      # Hitung setiap perbandingan elemen dari low sampai high-1, bandingkan dengan pivot
        if arr[j] >= pivot:         # Jika elemen j >= pivot, ia masuk bagian kiri (descending)
            i += 1                  # Geser batas kiri satu langkah
            arr[i], arr[j] = arr[j], arr[i]     # Pindahkan elemen ke sisi kiri
            swaps_count += 1

# ── Tempatkan Pivot ke Posisi Finalnya ────────────────────────────────────
    arr[i + 1], arr[high] = arr[high], arr[i + 1]   # Semua elemen >= pivot sudah di kiri (index low..i)
    swaps_count += 1                                # Tempatkan pivot tepat setelah batas tersebut (index i+1)

    return i + 1    # Kembalikan index posisi final pivot

# ── Quick Sort Rekursif ───────────────────────────────────────────────────────
def quick_sort_recursive(arr, low, high):
    if low < high:      #Base case: berhenti jika partisi <= 1 elemen
        pi = partition(arr, low, high)              # Partisi array dan dapatkan posisi final pivot
        quick_sort_recursive(arr, low, pi - 1)      # Rekursif urutkan bagian kiri dari pivot (elemen >= pivot)
        quick_sort_recursive(arr, pi + 1, high)     # Rekursif urutkan bagian kanan dari pivot (elemen < pivot)

# ── Quick Sort (Entry Point) ──────────────────────────────────────────────────
def quick_sort(data):
    global swaps_count, comparisons_count
    # Reset counter sebelum mulai agar tidak tercampur dengan pemanggilan sebelumnya
    swaps_count = 0
    comparisons_count = 0

    arr = data.copy()   # Salin data agar data asli tidak berubah

    start = time.perf_counter()     # Ukur waktu eksekusi dari awal hingga rekursi selesai
    quick_sort_recursive(arr, 0, len(arr) - 1)
    elapsed = (time.perf_counter() - start) * 1000      # Konversi detik → milidetik

    return {    # Kembalikan hasil dalam format dict yang konsisten dengan algoritma lainnya
        'name': 'Quick Sort (Median Sejati)',
        'sorted': arr, 
        'swaps': swaps_count, 
        'comparisons': comparisons_count, 
        'time': round(elapsed, 2)   
    }