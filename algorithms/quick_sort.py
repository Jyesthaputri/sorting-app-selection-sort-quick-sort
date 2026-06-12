# Cara kerja:
    # - Pilih pivot menggunakan Median of Three (elemen low, mid, high)
    # - Partisi array: elemen ≥ pivot ke kiri, elemen < pivot ke kanan
    # - Rekursi pada sub-array kiri dan kanan secara terpisah
# Perbandingan dengan varian Quick Sort lainnya:
    # - Pivot Pertama   → sederhana, sama rentannya dengan Pivot Terakhir terhadap worst case jika data sudah terurut
    # - Pivot Terakhir  → sama persis, hanya beda posisi pivot awal
    # - Median of Three → pivot dari 3 kandidat, lebih stabil
    # - Median Sejati   → pivot nilai tengah sesungguhnya, paling seimbang
# Kompleksitas Waktu : O(n log n) rata-rata, O(n²) worst case
# Kompleksitas Ruang : O(log n) — stack rekursi

import time     # Digunakan untuk mengukur waktu eksekusi secara akurat

swaps_count = 0             # Variabel global untuk melacak jumlah swap dan comparison lintas pemanggilan rekursi
comparisons_count = 0       # Direset ke 0 setiap kali quick_sort() dipanggil agar tidak terakumulasi antar run

# ── Median of Three ─────────────────────────────────────────────────
def median_of_three(arr, low, high):    
    # Memilih pivot yang lebih optimal dengan mengambil nilai median dari tiga kandidat: arr[low], arr[mid], arr[high].
    global swaps_count         
    mid = (low + high) // 2     # Index elemen tengah sub-array

# ── Langkah 1: Urutkan arr[low] dan arr[mid] secara descending ────────────
    # Pastikan arr[low] ≥ arr[mid]
    # Tujuan: median akan berada di posisi 'mid'
    if arr[low] < arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
        swaps_count += 1
# ── Langkah 2: Urutkan arr[low] dan arr[high] secara descending ──────────
    # Pastikan arr[low] adalah yang terbesar dari ketiganya
    if arr[low] < arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
        swaps_count += 1
# ── Langkah 3: Urutkan arr[mid] dan arr[high] secara descending ──────────
    # Setelah langkah ini: arr[low] ≥ arr[mid] ≥ arr[high]
    # Sehingga arr[mid] adalah nilai MEDIAN dari ketiganya
    if arr[mid] < arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
        swaps_count += 1
# Setelah 3 langkah di atas: - arr[low]  = terbesar dari ketiganya
                            #- arr[mid]  = median (pivot kita)
                            #- arr[high] = terkecil dari ketiganya
# ── Langkah 4: Pindahkan median ke arr[high] ─────────────────────────────
    # Logika partition mengasumsikan pivot ada di arr[high],
    # jadi kita pindahkan median ke sana agar partition tidak perlu diubah
    arr[mid], arr[high] = arr[high], arr[mid]
    swaps_count += 1

# ── DIUBAH: partition sekarang pakai median of three ─────────────────────────
#    Mempartisi sub-array arr[low..high] berdasarkan pivot (arr[high]).
#    Elemen ≥ pivot dipindahkan ke kiri pivot, elemen < pivot ke kanan.
def partition(arr, low, high):
    global swaps_count, comparisons_count

    # Tentukan pivot dengan median of three sebelum partisi
    if high - low >= 2:  # minimal 3 elemen agar median of three bermakna
        median_of_three(arr, low, high)

    pivot = arr[high]  # Pivot adalah arr[high] (sudah diset oleh median_of_three)
    i = low - 1        # i adalah batas kanan dari zona "≥ pivot" yang sedang dibangun

# ── Loop Partisi ──────────────────────────────────────────────────────────
    # Pindahkan semua elemen yang ≥ pivot ke sisi kiri
    for j in range(low, high):
        comparisons_count += 1      # Hitung setiap perbandingan
        if arr[j] >= pivot:         # descending, jika elemen ≥ pivot → masuk zona kiri
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            swaps_count += 1
    
# ── Tempatkan Pivot ke Posisi Akhirnya ────────────────────────────────────
    # Setelah loop, posisi i+1 adalah tempat pivot yang benar:
    # - Semua elemen di kiri i+1 bernilai ≥ pivot
    # - Semua elemen di kanan i+1 bernilai < pivot
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    swaps_count += 1

    return i + 1        # Kembalikan index posisi akhir pivot

# ── Rekursi Quick Sort, jika low >= high, sub-array hanya 1 elemen → sudah terurut ─────
def quick_sort_recursive(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)               # Partisi array dan dapatkan posisi akhir pivot
        quick_sort_recursive(arr, low, pi - 1)       # Rekursi pada sub-array KIRI (elemen-elemen yang ≥ pivot)
        quick_sort_recursive(arr, pi + 1, high)      # Rekursi pada sub-array KANAN (elemen-elemen yang < pivot)

# ── Fungsi Utama Quick Sort, Mengurutkan data dari nilai tertinggi ke terendah (descending) ───────
def quick_sort(data):
    global swaps_count, comparisons_count
    swaps_count = 0             # Reset counter setiap kali fungsi dipanggil
    comparisons_count = 0       # agar tidak terakumulasi dari pemanggilan sebelumnya

    arr = data.copy()        # Salin data agar array asli tidak berubah

    start = time.perf_counter()      # Ukur waktu eksekusi
    quick_sort_recursive(arr, 0, len(arr) - 1)
    elapsed = (time.perf_counter() - start) * 1000      # Konversi detik → milidetik

    return {        # Kembalikan hasil dalam format dict yang konsisten dengan algoritma lainnya
        'name': 'Quick Sort (Median of Three)',
        'sorted': arr,
        'swaps': swaps_count,
        'comparisons': comparisons_count, 
        'time': round(elapsed, 2)   
    }