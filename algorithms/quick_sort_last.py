# Cara kerja:
    # - Selalu menggunakan elemen TERAKHIR (arr[high]) sebagai pivot
    # - Partisi array: elemen >= pivot ke kiri, elemen < pivot ke kanan
    # - Rekursif urutkan bagian kiri dan kanan dari pivot
# Perbandingan dengan varian Quick Sort lainnya:
    # - Pivot Pertama   → sederhana, sama rentannya dengan Pivot Terakhir terhadap worst case jika data sudah terurut
    # - Pivot Terakhir  → sama persis, hanya beda posisi pivot awal
    # - Median of Three → pivot dari 3 kandidat, lebih stabil
    # - Median Sejati   → pivot nilai tengah sesungguhnya, paling seimbang
# Kompleksitas Waktu : O(n log n) rata-rata, O(n²) worst case (worst case terjadi jika data sudah terurut ascending/descending)
# Kompleksitas Ruang : O(log n) — stack rekursi

import time     # Digunakan untuk mengukur waktu eksekusi secara akurat

swaps_count = 0             # Variabel global untuk melacak jumlah swap dan comparison lintas rekursi
comparisons_count = 0       # Direset ke 0 setiap kali quick_sort() dipanggil dari awal

def partition(arr, low, high):  # Mempartisi array sehingga:
    global swaps_count, comparisons_count   
    pivot = arr[high]   # Gunakan elemen terakhir sebagai pivot (strategi Last Element)
    i = low - 1         # Dimulai dari low-1 karena belum ada elemen yang diproses

    for j in range(low, high):  # Loop Partisi (Scan setiap elemen dari low sampai high-1, bandingkan dengan pivot)
        comparisons_count += 1  # Hitung setiap perbandingan
        if arr[j] >= pivot:     # Jika elemen j >= pivot, ia masuk bagian kiri (descending)
            i += 1              # Geser batas kiri satu langkah
            arr[i], arr[j] = arr[j], arr[i]     # Pindahkan elemen ke sisi kiri
            swaps_count += 1                    # Hitung swap ini

    arr[i + 1], arr[high] = arr[high], arr[i + 1]   # Tempatkan Pivot ke Posisi Finalnya, Semua elemen >= pivot sudah di kiri (index low..i)
    swaps_count += 1                                # Tempatkan pivot tepat setelah batas tersebut (index i+1)

    return i + 1    # Kembalikan index posisi final pivot

def quick_sort_recursive(arr, low, high):       # Quick Sort Rekursif
    if low < high:                              # Base case: berhenti jika partisi <= 1 elemen
        pi = partition(arr, low, high)          # Partisi array dan dapatkan posisi final pivot
        quick_sort_recursive(arr, low, pi - 1)  # Rekursif urutkan bagian kiri dari pivot (elemen >= pivot)
        quick_sort_recursive(arr, pi + 1, high) # Rekursif urutkan bagian kanan dari pivot (elemen < pivot)

def quick_sort(data):       # Quick Sort (Entry Point)
    global swaps_count, comparisons_count
    swaps_count = 0         # Reset counter sebelum mulai agar tidak tercampur dengan pemanggilan sebelumnya
    comparisons_count = 0

    arr = data.copy()       # Salin data agar data asli tidak berubah

    start = time.perf_counter()     # Ukur waktu eksekusi dari awal hingga rekursi selesai
    quick_sort_recursive(arr, 0, len(arr) - 1)
    elapsed = (time.perf_counter() - start) * 1000  # Konversi detik → milidetik

    return {        # Kembalikan hasil dalam format dict yang konsisten dengan algoritma lainnya
        'name': 'Quick Sort (Pivot Terakhir)',
        'sorted': arr,
        'swaps': swaps_count, 
        'comparisons': comparisons_count,
        'time': round(elapsed, 2) 
    }