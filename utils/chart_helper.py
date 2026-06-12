# Untuk generate chart perbandingan algoritma sorting dan menyimpannya sebagai file PNG di folder assets/

import matplotlib
matplotlib.use('Agg')  # Wajib dipanggil SEBELUM import pyplot dan "Agg" wajib untuk Kivy, agar tidak conflict dengan display
import matplotlib.pyplot as plt
import numpy as np      # Tersedia untuk operasi numerik jika dibutuhkan

# Warna untuk masing-masing algoritma (sesuai dashboard)
COLORS = {
    'Quick Sort':     '#FF4444',  # merah
    'Selection Sort': '#F39C12',  # oranye
}

def get_color_list(results):    # Mengambil warna yang sesuai untuk setiap algoritma dalam results.
    return [COLORS.get(r['name'], '#AAAAAA') for r in results]  # Jika tidak ditemukan, gunakan '#AAAAAA' (abu-abu) sebagai fallback


# ── 1. Bar Chart Waktu Eksekusi ──────────────────────────────────────────────
def generate_bar_time(results, save_path='assets/chart_time.png'):
    names = [r['name'] for r in results]     # Ekstrak nama algoritma dan waktu eksekusi dari hasil sorting
    times = [r['time'] for r in results]
    colors = get_color_list(results)

    fig, ax = plt.subplots(figsize=(7, 4))   # Buat figure dan axes dengan ukuran 7x4 inci
    bars = ax.bar(names, times, color=colors, width=0.5)    # Gambar bar chart vertikal

    # Tambahkan label nilai di atas bar
    for bar, val in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width() / 2,      # Posisi X: tengah batang
                bar.get_height() + 0.1,                 # Posisi Y: sedikit di atas puncak
                f'{val}', ha='center', va='bottom', fontsize=9, fontweight='bold')  # Teks: nilai waktu

    # Styling chart
    ax.set_ylabel('Waktu (ms)')
    ax.set_title('Perbandingan Waktu Eksekusi')
    ax.set_facecolor('#F8F9FA')         # Background abu-abu sangat terang
    fig.tight_layout()                    # Sesuaikan layout otomatis agar tidak ada elemen terpotong
    plt.savefig(save_path, dpi=100, bbox_inches='tight')     # Simpan chart ke file PNG dan tutup figure untuk bebaskan memori
    plt.close()                                              # Wajib ditutup agar tidak terjadi memory leak


# ── 2. Pie Chart Distribusi Waktu ────────────────────────────────────────────
def generate_pie_time(results, save_path='assets/chart_pie.png'):
    # Ekstrak nama algoritma dan waktu eksekusi dari hasil sorting
    names = [r['name'] for r in results]
    times = [r['time'] for r in results]
    colors = get_color_list(results)

    fig, ax = plt.subplots(figsize=(5, 5))      # Buat figure berbentuk persegi agar pie chart tidak lonjong
    ax.pie(times, labels=None, colors=colors, autopct='%1.1f%%',    # Struktur Gambar pie chart
           startangle=140, pctdistance=0.75)
    ax.legend(names, loc='lower center', bbox_to_anchor=(0.5, -0.15),   # Letak legend di bawah chart dengan 2 kolom
              ncol=2, fontsize=8)
    ax.set_title('Distribusi Waktu (%)')
    fig.tight_layout()      # Sesuaikan layout dan simpan
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close()


# ── 3. Bar Chart Swaps horizontal perbandingan jumlah swap semua algoritma ───────────
def generate_bar_swaps(results, save_path='assets/chart_swaps.png'):
    names = [r['name'] for r in results]    # Ekstrak nama algoritma dan jumlah swap dari hasil sorting
    swaps = [r['swaps'] for r in results]
    colors = get_color_list(results)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(names, swaps, color=colors)     # Gambar bar chart HORIZONTAL (barh) agar nama algoritma tidak tumpang tindih
    ax.set_xlabel('Jumlah Swaps')           # Label sumbu X (nilai)
    ax.set_title('Perbandingan Swaps')
    ax.set_facecolor('#F8F9FA')
    fig.tight_layout()                      # Styling chart
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close()


# ── 4. Bar Chart Comparisons ─────────────────────────────────────────────────
def generate_bar_comparisons(results, save_path='assets/chart_comparisons.png'):
    names = [r['name'] for r in results]        # Ekstrak nama algoritma dan jumlah comparison dari hasil sorting
    comps = [r['comparisons'] for r in results]
    colors = get_color_list(results)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(names, comps, color=colors)     # Gambar bar chart HORIZONTAL (barh) agar nama algoritma tidak tumpang tindih
    ax.set_xlabel('Jumlah Comparisons')     # Label sumbu X (nilai)
    ax.set_title('Perbandingan Comparisons')
    ax.set_facecolor('#F8F9FA')
    fig.tight_layout()                      # Styling chart
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close()


# ── Generate semua chart sekaligus ───────────────────────────────────────────
def generate_all_charts(results):
    import os                               # Buat folder assets/ jika belum ada
    os.makedirs('assets', exist_ok=True)    # exist_ok=True: tidak error jika folder sudah ada

    # Generate semua chart satu per satu
    generate_bar_time(results)          # Chart 1: waktu eksekusi
    generate_pie_time(results)          # Chart 2: distribusi waktu
    generate_bar_swaps(results)         # Chart 3: jumlah swaps
    generate_bar_comparisons(results)   # Chart 4: jumlah comparisons
    print("Semua chart berhasil dibuat di folder assets/")