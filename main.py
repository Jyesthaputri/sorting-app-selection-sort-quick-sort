import sys  # Modul bawaan Python untuk akses argumen & keluar aplikasi (sys.exit)
import os   # Modul bawaan Python untuk operasi file & direktori (cek path, nama file)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    # QApplication=app utama, QMainWindow=jendela utama, QWidget=widget dasar, QVBoxLayout=layout vertikal
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    # QHBoxLayout=layout horizontal, QLabel=teks, QLineEdit=input teks, QPushButton=tombol
    QScrollArea, QFrame, QGridLayout,
    # QScrollArea=area scroll, QFrame=bingkai/garis, QGridLayout=layout grid
    QStackedWidget
    # QStackedWidget=widget multi-halaman (seperti tab tapi tanpa tab bar)
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
# Qt=konstanta alignment dll, QThread=thread terpisah, pyqtSignal=sinyal antar thread
from PyQt5.QtGui import QFont   # QFont=pengaturan font teks
from visualizers import (
    SortingVisualizerPage,          # Halaman visualisasi Selection Sort
    QuickSortVisualizerPage,        # Halaman visualisasi Quick Sort (Median of Three)
    QuickSortFirstVisualizerPage,   # Halaman visualisasi Quick Sort (Pivot Pertama)
    QuickSortLastVisualizerPage,    # Halaman visualisasi Quick Sort (Pivot Terakhir)
    QuickSortTrueVisualizerPage     # Halaman visualisasi Quick Sort (Median Sejati)
)
from algorithms import (
    selection_sort,         # Fungsi algoritma Selection Sort
    quick_sort_first,       # Fungsi Quick Sort dengan pivot elemen pertama
    quick_sort_last,        # Fungsi Quick Sort dengan pivot elemen terakhir
    quick_sort_mot,         # Fungsi Quick Sort dengan pivot Median of Three
    quick_sort_true         # Fungsi Quick Sort dengan pivot Median Sejati
)
from utils import load_xlsx, save_xlsx      # Fungsi baca & simpan file Excel
from chart_widget import BarChartWidget     # Widget bar chart custom untuk visualisasi perbandingan waktu
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas    # Canvas matplotlib agar bisa ditempel di PyQt5
from matplotlib.figure import Figure        # Objek Figure matplotlib untuk membuat grafik

class SortWorker(QThread):  #Menjalankan semua algoritma sorting di thread terpisah agar UI tidak freeze
    finished = pyqtSignal(list)     # Sinyal dikirim ke UI saat sorting selesai, membawa list hasil
    error = pyqtSignal(str)         # Sinyal dikirim ke UI jika terjadi error, membawa pesan error

    def __init__(self, file_path):
        super().__init__()          # Inisialisasi QThread
        self.file_path = file_path  # Simpan path file Excel yang akan diproses
        self.df = None              # Placeholder DataFrame (diisi saat run)
        self.original_data = None   # Placeholder data asli sebelum sorting

    def run(self):      # Otomatis dipanggil saat .start() → berjalan di thread terpisah
        try:
            data, self.df = load_xlsx(self.file_path)   # Baca file Excel, ambil kolom Keaktifan & DataFrame lengkap
            
            clean_data = [x for x in data if isinstance(x, (int, float))]   # Buang nilai non-angka (NaN, teks, dll)
            if len(clean_data) == 0:
                raise Exception("Data kosong / tidak ada angka yang bisa diurutkan.")
            
            self.original_data = clean_data[:100]   # Batasi ukuran area data untuk keperluan visualisasi animasi
            
            algos = [     # Daftar semua fungsi sorting yang akan dijalankan
                quick_sort_first,
                quick_sort_last,
                quick_sort_mot,
                quick_sort_true,
                selection_sort
            ]
            # Jalankan semua algoritma, tiap fn() mengembalikan dict {name, time, swaps, comparisons, sorted}
            results = [fn(clean_data) for fn in algos]
            results.sort(key=lambda x: x['time'])   # Urutkan hasil berdasarkan waktu tercepat ke terlambat
            self.finished.emit(results)             # Kirim hasil ke UI via sinyal finished

        except Exception as e:
            self.error.emit(str(e))     # Kirim pesan error ke UI via sinyal error


# ── Helper card ───────────────────────────────────────────────────────────────
# Membungkus layout apapun menjadi card berdesain putih dengan border biru
def make_card(layout, min_height=None):
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background: white;
            border-radius: 14px;
            border: 1px solid #D0D7FF;
        }
    """)        # Styling card: putih, sudut membulat, border biru muda    
    if min_height:
        card.setMinimumHeight(min_height)   # Set tinggi minimum jika diberikan
    card.setLayout(layout)                  # Pasang layout ke dalam card
    return card                             # Kembalikan card siap pakai

# ── Main Window ───────────────────────────────────────────────────────────────
class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dashboard Perbandingan Algoritma Selection Sort & Quick Sort')

        self.results = []                       # Menyimpan hasil sorting semua algoritma
        self.df = None                          # Menyimpan DataFrame dari file Excel
        self.file_path = ''                     # Menyimpan path file yang diinput user
        self.col_stretch = [1, 3, 2, 2, 2, 3]   # Proporsi lebar kolom tabel

        self.quick_first_page = None            # Placeholder halaman visualisasi (diisi di _build_ui)
        self.quick_last_page = None
        self.quick_mot_page = None
        self.quick_true_page = None

        self._build_ui()                # Bangun semua komponen UI
        self.showMaximized()            # Tampilkan jendela dalam mode fullscreen

    def _update_time_chart(self):   # Perbarui semua chart perbandingan waktu setelah sorting selesai
        if not self.results:
            return

        # Ambil selection sort
        selection = next((r for r in self.results if r['name'] == 'Selection Sort'), None)  # Cari hasil Selection Sort dari list
        if not selection:
            return

        chart_map = {   # Mapping nama algoritma → nama atribut chart yang sesuai
            'Quick Sort (Pivot Pertama)':   'chart_vs_first',
            'Quick Sort (Pivot Terakhir)':  'chart_vs_last',
            'Quick Sort (Median of Three)': 'chart_vs_mot',
            'Quick Sort (Median Sejati)':   'chart_vs_true',
        }

        for qs_name, chart_attr in chart_map.items():   # Update tiap chart dengan data waktu Selection Sort vs Quick Sort
            qs = next((r for r in self.results if r['name'] == qs_name), None)
            if qs and hasattr(self, chart_attr):
                labels = ['Selection Sort', qs_name.replace('Quick Sort ', '')]
                values = [selection['time'], qs['time']]
                getattr(self, chart_attr).update_chart(labels, values)
    
    # ── Build UI: Susun layout utama (sidebar kiri + halaman kanan) ─────────────────
    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet('background: #EEF2FF;')  # Background ungu muda untuk seluruh jendela
        self.setCentralWidget(root)

        main = QHBoxLayout(root)                    # Layout horizontal: sidebar | halaman
        main.setSpacing(10)
        main.setContentsMargins(0, 0, 10, 10)

        self.sidebar = self._build_sidebar()        # Bangun sidebar kiri
        main.addWidget(self.sidebar, stretch=20)    # Sidebar ambil 20% lebar

        self.pages = QStackedWidget()               # Panel kanan menggunakan stacked widget (multi page)
        main.addWidget(self.pages, stretch=80)      # Konten kanan ambil 80% lebar

        self.dashboard_page = self._build_right_panel()
        self.pages.addWidget(self.dashboard_page)   # Index 0: halaman dashboard utama

        self.quick_first_page = QuickSortFirstVisualizerPage()
        self.pages.addWidget(self.quick_first_page)  # Index 1: visualisasi Quick Sort pivot pertama

        self.quick_last_page = QuickSortLastVisualizerPage()
        self.pages.addWidget(self.quick_last_page)   # Index 2: visualisasi Quick Sort pivot terakhir

        self.quick_page = QuickSortVisualizerPage()
        self.pages.addWidget(self.quick_page)        # Index 3: visualisasi Quick Sort Median of Three

        self.quick_true_page = QuickSortTrueVisualizerPage()
        self.pages.addWidget(self.quick_true_page)   # Index 4: visualisasi Quick Sort Median Sejati

        self.visualizer_page = SortingVisualizerPage()
        self.pages.addWidget(self.visualizer_page)   # Index 5: visualisasi Selection Sort

    # ── Sideba: Navigasi, input file, tombol run & download ───────────────
    def _build_sidebar(self):
        sidebar = QWidget()
        sidebar.setStyleSheet('background: #1A3F8C;')   # Background biru tua untuk sidebar
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        def lbl(text, color='white', size=12, bold=False, align=Qt.AlignLeft, wrap=False):
            l = QLabel(text)                            # Helper lokal untuk buat QLabel dengan styling cepat
            weight = 'bold' if bold else 'normal'
            l.setStyleSheet(f'color: {color}; font-size: {size}px; font-weight: {weight};')
            l.setAlignment(align)
            if wrap:
                l.setWordWrap(True)
            return l

        layout.addWidget(lbl('☰  DASHBOARD\nSorting Algorithm',
                             size=14, bold=True, align=Qt.AlignCenter))     # Judul sidebar
        layout.addWidget(self._separator())               # Garis pemisah  

        # MENU NAVIGASI
        layout.addWidget(lbl("📌 MENU", color="yellow", bold=True))

        btn_dashboard = QPushButton("🏠 Dashboard")
        btn_dashboard.setFixedHeight(35)
        btn_dashboard.setStyleSheet("""
            QPushButton {
                background:white;
                border-radius:6px;
                font-size:12px;
                font-weight:bold;
            }
            QPushButton:hover { background:#D6E4FF; }
        """)
        btn_dashboard.clicked.connect(lambda: self.pages.setCurrentIndex(0))    # Klik → pindah ke halaman index 0 (dashboard)
        layout.addWidget(btn_dashboard)

        for label, index in [           # Loop buat tombol navigasi untuk tiap varian Quick Sort
            ("Quick Sort (Pivot Pertama)",   1),
            ("Quick Sort (Pivot Terakhir)",  2),
            ("Quick Sort (Median of Three)", 3),
            ("Quick Sort (Median Sejati)",   4),
        ]:
            btn = QPushButton(label)
            btn.setFixedHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background:white;
                    border-radius:6px;
                    font-size:11px;
                    font-weight:bold;
                }
                QPushButton:hover { background:#D6E4FF; }
            """)
            btn.clicked.connect(lambda _, i=index: self.pages.setCurrentIndex(i))   # i=index: tangkap nilai loop agar tidak ter-overwrite
            layout.addWidget(btn)

        btn_selection = QPushButton("Selection Sort")
        btn_selection.setFixedHeight(35)
        btn_selection.setStyleSheet("""
            QPushButton {
                background:white;
                border-radius:6px;
                font-size:12px;
                font-weight:bold;
            }
            QPushButton:hover { background:#D6E4FF; }
        """)
        btn_selection.clicked.connect(lambda: self.pages.setCurrentIndex(5))    # Klik → pindah ke halaman index 5 (Selection Sort)
        layout.addWidget(btn_selection)

        layout.addWidget(self._separator())

        # INPUT FILE
        layout.addWidget(lbl('TEMPELKAN FILE ANDA:', color='yellow', bold=True))

        self.txt_file = QLineEdit()
        self.txt_file.setPlaceholderText('Paste path file .xlsx disini')
        self.txt_file.setStyleSheet(
            'background:white; border-radius:5px; padding:5px; font-size:11px;')
        self.txt_file.textChanged.connect(self._on_file_input)      # Setiap teks berubah → validasi path file
        layout.addWidget(self.txt_file)

        self.lbl_file_status = QLabel('')       # Label status file (✅ valid / ❌ tidak ditemukan)
        self.lbl_file_status.setStyleSheet('color:white; font-size:11px;')
        self.lbl_file_status.setWordWrap(True)
        layout.addWidget(self.lbl_file_status)

        layout.addWidget(self._separator())
        layout.addWidget(lbl('✦  ALGORITMA', bold=True, size=13))

        for name, color in [        # Tampilkan daftar algoritma dengan warna masing-masing
            ('🟠  Selection Sort', '#F39C12'),
            ('🔴  Quick Sort', '#FF6B6B'),
        ]:
            layout.addWidget(lbl(name, color=color, size=12))

        layout.addWidget(self._separator())

        # BUTTON RUN
        self.btn_run = QPushButton('▶  Jalankan Semua')
        self.btn_run.setFixedHeight(42)
        self.btn_run.setStyleSheet("""
            QPushButton {
                background:#3478F6; color:white;
                font-weight:bold; font-size:13px;
                border-radius:8px;
            }
            QPushButton:hover    { background:#2563EB; }
            QPushButton:disabled { background:#555; color:#aaa; }
        """)
        self.btn_run.clicked.connect(self._run_all)     # Klik → jalankan semua algoritma sorting
        layout.addWidget(self.btn_run)

        layout.addWidget(self._separator())
        layout.addWidget(lbl('DOWNLOAD FILE\nYANG SUDAH TERURUT:',
                             color='yellow', bold=True, align=Qt.AlignCenter))

        self.txt_download = QLineEdit()
        self.txt_download.setPlaceholderText('Nama file output (opsional)')
        self.txt_download.setStyleSheet(
            'background:white; border-radius:5px; padding:5px; font-size:11px;')
        layout.addWidget(self.txt_download)

        btn_dl = QPushButton('💾  Download')
        btn_dl.setFixedHeight(38)
        btn_dl.setStyleSheet("""
            QPushButton {
                background:#1A9E4F; color:white;
                font-weight:bold; border-radius:8px; font-size:12px;
            }
            QPushButton:hover { background:#158040; }
        """)
        btn_dl.clicked.connect(self._download_result)   # Klik → simpan hasil sorting ke file Excel
        layout.addWidget(btn_dl)

        self.lbl_dl_status = QLabel('')             # Label status download (✅ berhasil / ⚠️ belum run)
        self.lbl_dl_status.setStyleSheet('color:white; font-size:11px;')
        self.lbl_dl_status.setWordWrap(True)
        layout.addWidget(self.lbl_dl_status)

        layout.addStretch()         # Dorong semua widget ke atas, sisa ruang di bawah kosong
        return sidebar

    def _separator(self):           # Buat garis horizontal pemisah antar section sidebar
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet('color: #3A5FAA;')
        return line

    # ── Panel kanan (Dashboard):  judul + cards + tabel + chart ─────────────
    def _build_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Judul dashboard (dibuat self supaya bisa diubah fontnya)
        self.lbl_dashboard_title = QLabel("DASHBOARD PERBANDINGAN SELECTION SORT DAN QUICK SORT")
        self.lbl_dashboard_title.setAlignment(Qt.AlignLeft)
        self.lbl_dashboard_title.setStyleSheet("color:#1A3F8C; font-size:22px; font-weight:bold;")
        layout.addWidget(self.lbl_dashboard_title)

        # Subjudul / keterangan studi kasus
        self.lbl_dashboard_subtitle = QLabel("Studi Kasus: Pengurutan Data Keaktifan Siswa (Tertinggi → Terendah)")
        self.lbl_dashboard_subtitle.setAlignment(Qt.AlignLeft)
        self.lbl_dashboard_subtitle.setStyleSheet("color:#333; font-size:15px; font-weight:bold;")
        layout.addWidget(self.lbl_dashboard_subtitle) 

        # Tambahkan baris 5 summary card
        layout.addWidget(self._build_summary_cards())

        # Card tabel hasil perbandingan (full lebar dan ambil 35% tinggi)
        layout.addWidget(self._build_table_card(), stretch=35)

        # Card chart perbandingan waktu (full lebar 2x2, ambil 65% tinggi)
        layout.addWidget(self._build_chart_card("PERBANDINGAN WAKTU EKSEKUSI", "chart_time"), stretch=65)

        return panel

    # ── Summary cards: 5 card ringkasan statistik hasil sorting ─────────────
    def _build_summary_cards(self):
        self.card_labels = {}       # Dict untuk simpan referensi QLabel nilai tiap card
        self.card_titles = {}       # Dict untuk simpan referensi QLabel judul tiap card

        row = QWidget()
        row.setFixedHeight(110)
        layout = QHBoxLayout(row)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        def add_card(key, title, subtitle=''):  # Helper lokal: buat satu card dan daftarkan ke dict
            v = QVBoxLayout()
            v.setContentsMargins(10, 8, 10, 8)
            v.setSpacing(3)

            t = QLabel(title)
            t.setAlignment(Qt.AlignCenter)
            t.setStyleSheet("color:#888; font-size:13px; font-weight:bold;")
            v.addWidget(t)

            val = QLabel("-")   # Nilai awal "-" → diupdate setelah sorting selesai
            val.setAlignment(Qt.AlignCenter)
            val.setWordWrap(True)
            val.setStyleSheet("color:#1A3F8C; font-size:18px; font-weight:bold;")
            v.addWidget(val)

            self.card_titles[key] = t       # Simpan referensi judul agar bisa diubah fontnya saat resize
            self.card_labels[key] = val     # Simpan referensi nilai agar bisa diupdate setelah sorting

            if subtitle:
                s = QLabel(subtitle)
                s.setAlignment(Qt.AlignCenter)
                s.setStyleSheet("color:#aaa; font-size:13px; font-weight:bold;")
                v.addWidget(s)

            layout.addWidget(make_card(v))
        # Model card pada dashboard
        add_card("avg_time", "🕐 Rata-rata Waktu", "Semua Algoritma")
        add_card("fastest", "⚡ Algoritma Tercepat", "")
        add_card("total_swaps", "🔄 Total Swaps", "Semua Algoritma")
        add_card("total_comps", "🔁 Total Comparisons", "Semua Algoritma")
        add_card("total_data", "👥 Jumlah Data", "Siswa")

        return row

    # ── Chart card:  Grid 2x2 bar chart perbandingan waktu ──────────────
    def _build_chart_card(self, title, chart_key):
        v = QVBoxLayout()
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(6)

        t = QLabel(title)
        t.setStyleSheet('color:#1A3F8C; font-size:16px; font-weight:bold;')
        t.setAlignment(Qt.AlignCenter)
        v.addWidget(t)
        self.lbl_chart_title = t        # Simpan referensi agar bisa diubah fontnya saat resize

        grid = QGridLayout()            # Grid 2x2 untuk 4 chart
        grid.setSpacing(10)

        chart_configs = [               # Konfigurasi 4 chart: nama atribut & judul masing-masing
            ("chart_vs_first", "Selection Sort vs Pivot Pertama"),
            ("chart_vs_last",  "Selection Sort vs Pivot Terakhir"),
            ("chart_vs_mot",   "Selection Sort vs Median of Three"),
            ("chart_vs_true",  "Selection Sort vs Median Sejati"),
        ]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]    # Posisi grid: baris & kolom tiap chart

        for (attr_name, chart_title), (row, col) in zip(chart_configs, positions):
            sub_v = QVBoxLayout()
            sub_v.setContentsMargins(6, 6, 6, 6)
            sub_v.setSpacing(4)

            sub_title = QLabel(chart_title)
            sub_title.setAlignment(Qt.AlignCenter)
            sub_title.setStyleSheet("color:#1A3F8C; font-size:11px; font-weight:bold;")
            sub_v.addWidget(sub_title)

            chart = BarChartWidget(title=chart_title)   # Buat widget bar chart untuk pasangan algoritma ini
            sub_v.addWidget(chart)

            sub_card = QFrame()
            sub_card.setStyleSheet("""
                QFrame {
                    background: #F8FAFF;
                    border-radius: 10px;
                    border: 1px solid #D0D7FF;
                }
            """)
            sub_card.setLayout(sub_v)

            grid.addWidget(sub_card, row, col)
            setattr(self, attr_name, chart)     # Simpan referensi chart ke atribut (chart_vs_first, dst)

        v.addLayout(grid)
        self.chart_time = getattr(self, 'chart_vs_first')   # Fallback agar kode lama tidak error
        return make_card(v)
    
    # ── Tabel card hasil perbandingan semua algoritma ─────────────────────
    def _build_table_card(self):
        v = QVBoxLayout()
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(6)

        t = QLabel("HASIL PERBANDINGAN")
        t.setStyleSheet("color:#1A3F8C; font-size:14px; font-weight:bold;")
        t.setAlignment(Qt.AlignCenter)
        v.addWidget(t)

        self.table_headers = []     # Simpan referensi semua QLabel header untuk update font saat resize
        self.table_rows = []        # Simpan referensi semua QLabel baris untuk update font saat resize

        header = QGridLayout()
        header.setSpacing(0)

        columns = ["No", "Algoritma", "Waktu (ms)", "Swaps", "Comparisons", "Performa"]
        col_stretch = [1, 3, 2, 2, 2, 3]

        for i, col in enumerate(columns):
            lh = QLabel(col)
            header.setColumnStretch(i, self.col_stretch[i])     # Atur proporsi lebar tiap kolom sesuai col_stretch
            lh.setStyleSheet(
                "color:#333; font-size:15px; font-weight:bold;"
                "border-bottom: 2px solid #ccc; padding:8px;"
            )
            header.addWidget(lh, 0, i)
            self.table_headers.append(lh)

        header_widget = QWidget()
        header_widget.setLayout(header)
        v.addWidget(header_widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")     # Hilangkan border scroll area agar menyatu dengan card

        self.tbl_container = QWidget()
        self.tbl_layout = QVBoxLayout(self.tbl_container)
        self.tbl_layout.setSpacing(5)
        self.tbl_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.tbl_container)
        v.addWidget(scroll)

        return make_card(v)

    # ── Resize event: update gambar saat window diubah ukurannya ─────────────
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_dashboard_fonts()      # Panggil update font setiap kali ukuran jendela berubah

    # ── Logic: Validasi file, jalankan sorting, update UI, download hasil ───────
    def _on_file_input(self, text):         # Dipanggil setiap teks di input file berubah
        path = text.strip()
        if os.path.exists(path):
            self.file_path = path
            self.lbl_file_status.setText(f'✅ {os.path.basename(path)}')    # Tampilkan nama file saja, bukan full path
            self.lbl_file_status.setStyleSheet('color:#00DD00; font-size:11px;')
        else:
            self.file_path = ''
            self.lbl_file_status.setText('❌ File tidak ditemukan')
            self.lbl_file_status.setStyleSheet('color:#FF6B6B; font-size:11px;')

    def _run_all(self):                     # Dipanggil saat tombol "Jalankan Semua" diklik
        if not self.file_path:
            self.lbl_file_status.setText('⚠️ Masukkan path file dulu!')
            self.lbl_file_status.setStyleSheet('color:orange; font-size:11px;')
            return

        self.btn_run.setText('⏳ Memproses...')
        self.btn_run.setDisabled(True)      # Nonaktifkan tombol agar tidak diklik dua kali

        self.worker = SortWorker(self.file_path)
        self.worker.finished.connect(self._on_done)     # Hubungkan sinyal finished → _on_done
        self.worker.error.connect(self._on_error)       # Hubungkan sinyal error → _on_error
        self.worker.start()                             # Mulai thread sorting

    def _on_done(self, results):            # Dipanggil otomatis saat SortWorker selesai
        self.results = results
        self.df = self.worker.df
        
        for r in results:
            print(f"name='{r['name']}' | time={r['time']} ms")  # Debug: cetak hasil tiap algoritma ke terminal

        self._update_summary()      # Update 5 summary card
        self._update_table()        # Update tabel perbandingan
        self._update_time_chart()   # Update 4 bar chart

        self.btn_run.setText('▶  Jalankan Semua')
        self.btn_run.setDisabled(False)     # Aktifkan kembali tombol run

        if self.worker.original_data:       # Kirim data ke setiap halaman visualisasi algoritma
            self.original_data = self.worker.original_data
            self.visualizer_page.set_data(self.worker.original_data)
            self.quick_page.set_data(self.worker.original_data)
            self.quick_first_page.set_data(self.worker.original_data)
            self.quick_last_page.set_data(self.worker.original_data)
            self.quick_true_page.set_data(self.worker.original_data)

    def _on_error(self, msg):               # Dipanggil jika SortWorker melempar exception
        self.lbl_file_status.setText(f'❌ Error: {msg}')
        self.lbl_file_status.setStyleSheet('color:#FF6B6B; font-size:11px;')
        self.btn_run.setText('▶  Jalankan Semua')
        self.btn_run.setDisabled(False)     # Aktifkan kembali tombol run meski error

    def _update_summary(self):              # Hitung & tampilkan statistik ringkasan ke 5 summary card
        avg = round(sum(r['time'] for r in self.results) / len(self.results), 2)    # Rata-rata waktu semua algoritma
        swap = sum(r['swaps'] for r in self.results)                                # Total swaps semua algoritma
        comp = sum(r['comparisons'] for r in self.results)                          # Total comparisons semua algoritma
        fast = self.results[0]                                                      # Algoritma tercepat (sudah diurutkan)

        self.card_labels['avg_time'].setText(f'{avg} ms')
        self.card_labels['fastest'].setText(f"{fast['name']}\n{fast['time']} ms")
        self.card_labels['fastest'].setStyleSheet(
            'color:#1A9E4F; font-size:13px; font-weight:bold;') # Warna hijau untuk algoritma tercepat
        self.card_labels['total_swaps'].setText(f'{swap:,}')    # Format angka dengan pemisah ribuan
        self.card_labels['total_comps'].setText(f'{comp:,}')
        self.card_labels['total_data'].setText(str(len(self.worker.original_data)))

    def _update_table(self):                # Hapus baris lama lalu isi ulang tabel dengan hasil terbaru
        for i in reversed(range(self.tbl_layout.count())):
            w = self.tbl_layout.itemAt(i).widget()
            if w:
                w.deleteLater()             # Hapus widget lama dari memori

        self.table_rows = []
        fastest_time = self.results[0]['time']  # Waktu tercepat sebagai pembanding relatif

        for i, r in enumerate(self.results, 1):
            relative = round(r['time'] / fastest_time, 2)
            rel_text = "⚡ Tercepat" if i == 1 else f"{relative}x lebih lambat" # Kolom performa relatif terhadap tercepat

            row_w = QWidget()
            row_l = QGridLayout(row_w)
            row_l.setSpacing(0)
            row_l.setContentsMargins(0, 4, 0, 4)

            cols = [str(i), r['name'], f"{r['time']} ms", f"{r['swaps']:,}", f"{r['comparisons']:,}", rel_text]

            for j, text in enumerate(cols):
                lbl = QLabel(text)
                lbl.setStyleSheet("color:#1A3F8C; font-size:15px; font-family:Courier New; font-weight:bold;")
                row_l.setColumnStretch(j, self.col_stretch[j])
                row_l.addWidget(lbl, 0, j)
                self.table_rows.append(lbl)         # Daftarkan ke list agar bisa diupdate fontnya saat resize
                
            self.tbl_layout.addWidget(row_w)

        self.tbl_layout.addStretch()
        self._update_dashboard_fonts()          # Langsung sinkronkan font setelah tabel diperbarui
    
    def _download_result(self):             # Simpan data hasil sorting terbaik ke file Excel
        if not self.results:
            self.lbl_dl_status.setText('⚠️ Jalankan algoritma dulu!')
            self.lbl_dl_status.setStyleSheet('color:orange; font-size:11px;')
            return

        path = self.txt_download.text().strip()
        if not path:
            path = 'hasil_terurut.xlsx'     # Nama default jika user tidak mengisi

        if not path.endswith('.xlsx'):      # Pastikan ekstensi file selalu .xlsx
            path += '.xlsx'

        save_xlsx(self.df, self.results[0]['sorted'], path)     # Simpan menggunakan hasil sorting algoritma tercepat
        self.lbl_dl_status.setText(f'✅ Disimpan: {path}')
        self.lbl_dl_status.setStyleSheet('color:#00DD00; font-size:11px;')

    def _update_dashboard_fonts(self):      # Hitung ukuran font responsif berdasarkan ukuran jendela
        w = self.width()
        h = self.height()
        base = min(w, h)                    # Pakai dimensi terkecil agar font tidak terlalu besar di layar lebar

        title_size = max(18, min(34, base // 32))
        subtitle_size = max(12, min(20, base // 60))
        card_title_size = max(10, min(16, base // 85))
        card_value_size = max(14, min(26, base // 45))
        table_header_size = max(13, min(18, base // 90))
        table_row_size = max(18, min(13, base // 100))

        # dashboard title
        if hasattr(self, "lbl_dashboard_title"):
            self.lbl_dashboard_title.setStyleSheet(
                f"color:#1A3F8C; font-size:{title_size}px; font-weight:bold;"
            )
        if hasattr(self, "lbl_dashboard_subtitle"):
            self.lbl_dashboard_subtitle.setStyleSheet(
                f"color:#555; font-size:{subtitle_size}px;font-weight:bold;"
            )
        if hasattr(self, "lbl_chart_title"):
            self.lbl_chart_title.setStyleSheet(
            f"color:#1A3F8C; font-size:{subtitle_size}px; font-weight:bold;"
    )
        # summary card title + value
        if hasattr(self, "card_titles"):
            for k in self.card_titles:
                self.card_titles[k].setStyleSheet(
                    f"color:#888; font-size:{card_title_size}px;"
                )
        if hasattr(self, "card_labels"):
            for k in self.card_labels:
                self.card_labels[k].setStyleSheet(
                    f"color:#1A3F8C; font-size:{card_value_size}px; font-weight:bold;"
                )
    # table headers
        if hasattr(self, "table_headers"):
            for lbl in self.table_headers:
                lbl.setStyleSheet(
                    f"color:#333; font-size:{table_header_size}px; font-weight:bold;"
                    "border-bottom: 1px solid #ccc; padding:6px;"
                )
    # table rows
        if hasattr(self, "table_rows"):
            for lbl in self.table_rows:
                lbl.setStyleSheet(
                    f"color:#1A3F8C; font-size:{table_row_size}px; font-family:Courier New; font-weight:bold;"
                )

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':        
    app = QApplication(sys.argv)        # Buat instance aplikasi PyQt5
    app.setFont(QFont('Segoe UI', 10))  # Set font default seluruh aplikasi
    window = DashboardWindow()          # Buat jendela utama
    window.showMaximized()              # Tampilkan fullscreen
    sys.exit(app.exec_())               # Tampilkan fullscreen