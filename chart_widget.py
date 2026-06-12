# Cara kerja:
# - Membungkus matplotlib Figure dan FigureCanvas ke dalam QWidget
# - Bisa dipanggil update_chart() kapan saja untuk memperbarui tampilan chart
# - Warna batang otomatis disesuaikan berdasarkan nama algoritma

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure    # Figure adalah kanvas gambar matplotlib


class BarChartWidget(QWidget):      # Widget PyQt5 yang menampilkan bar chart matplotlib secara inline.
    def __init__(self, title="Chart"):
        super().__init__()

        self.title = title      # Judul chart, ditampilkan di atas batang

        # ── Figure & Canvas ───────────────────────────────────────────
        self.figure = Figure(facecolor='#F8FAFF')   # Figure adalah objek gambar matplotlib tempat semua elemen chart digambar
        self.canvas = FigureCanvas(self.figure)     # Canvas adalah jembatan penampil antara matplotlib Figure dan widget PyQt5

        # Biarkan canvas mengikuti ukuran parent widget
        self.canvas.setSizePolicy(
            QSizePolicy.Expanding,      # Horizontal: ikuti lebar parent
            QSizePolicy.Expanding       # Vertical: ikuti tinggi parent
        )
        
        layout = QVBoxLayout(self)      # Tambahkan canvas ke layout widget ini
        layout.setContentsMargins(0, 0, 0, 0)   # Margin 0 agar chart mengisi seluruh area tanpa padding tambahan
        layout.addWidget(self.canvas)

    def update_chart(self, labels, values):     # Memperbarui tampilan bar chart dengan data baru
        self.figure.clear()                 # Bersihkan figure dari gambar sebelumnya sebelum menggambar ulang
        ax = self.figure.add_subplot(111)   # Buat subplot baru (111 = 1 baris, 1 kolom, subplot ke-1)

        # ── Warna batang ──────────────────────────────────────────────
        colors = []
        for label in labels:        # Warna disesuaikan otomatis berdasarkan nama algoritma:
            if 'Selection' in label:
                colors.append('#F39C12')    # Oranye untuk Selection Sort
            else:
                colors.append('#3478F6')    # Biru untuk Quick Sort dan varian lainnya

        # ── Gambar batang ─────────────────────────────────────────────
        bars = ax.bar(
            labels, values,
            color=colors,       # Warna masing-masing batang
            width=0.45,         # Lebar batang (0-1, makin besar makin lebar)
            edgecolor='white',  # Warna border batang
            linewidth=1.2,      # Ketebalan border batang
            zorder=3            # Urutan layer: batang digambar di atas grid
        )

        # ── Styling sumbu ─────────────────────────────────────────────
        ax.set_facecolor('#F8FAFF')             # Background area plot
        ax.set_ylabel("Waktu (ms)", fontsize=9, color='#444')   # Label sumbu Y
        ax.tick_params(axis='x', labelsize=8, colors='#333')    # Styling tick sumbu X
        ax.tick_params(axis='y', labelsize=8, colors='#333')    # Styling tick sumbu Y

        # Wrap label panjang agar tidak tumpang tindih
        wrapped = []
        for lbl in labels:
            if len(lbl) > 14:   # Jika nama algoritma lebih dari 14 karakter, potong di spasi pertama
                wrapped.append(lbl.replace(' ', '\n', 1))       # Ganti spasi pertama dengan newlin
            else:
                wrapped.append(lbl)     # dan lanjutkan ke baris baru agar tidak tumpang tindih antar label
        
        # Terapkan label yang sudah di-wrap ke sumbu X
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(wrapped, fontsize=8)

        # ── Grid ──────────────────────────────────────────────────────
        # Grid horizontal saja (sumbu Y) agar mudah membaca nilai batang
        ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#CCCCCC', zorder=0)
        ax.set_axisbelow(True)      # Pastikan grid selalu di belakang batang
        
        ax.spines['top'].set_visible(False)     # Hilangkan border kanan dan atas agar tampilan lebih bersih (minimalis)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CCCCCC')      # Border kiri warna abu-abu terang
        ax.spines['bottom'].set_color('#CCCCCC')    # Border bawah warna abu-abu terang

        # ── Tampilkan nilai waktu tepat di atas setiap batang agar mudah dibaca ─────
        max_val = max(values) if values else 1      # Hindari pembagian dengan 0 jika values kosong
        for i, (bar, v) in enumerate(zip(bars, values)):
            ax.text(
                bar.get_x() + bar.get_width() / 2,      # Posisi X: tengah batang
                v + max_val * 0.02,                     # Posisi Y: sedikit di atas puncak batang
                f"{v} ms",                              # Teks: nilai waktu dengan satuan ms
                ha='center', va='bottom',               # Alignment: tengah horizontal, bawah vertikal
                fontsize=8, fontweight='bold',
                color='#1A3F8C'                       # Warna teks: biru tua
            )

        # Beri ruang di atas batang agar label tidak terpotong
        ax.set_ylim(0, max_val * 1.25)  # Tinggi maksimum sumbu Y = 125% dari nilai terbesar

        # ── Padding figure ────────────────────────────────────────────
        self.figure.tight_layout(pad=1.2)   # tight_layout menyesuaikan padding otomatis agar tidak ada elemen terpotong
        self.canvas.draw()                  # Render ulang canvas ke layar dengan data terbaru