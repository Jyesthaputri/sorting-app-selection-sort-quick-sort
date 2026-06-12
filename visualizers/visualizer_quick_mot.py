from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QGridLayout, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer


# ── Generator Quick Sort Step-by-Step (DESCENDING) ────────────────────────────
def quick_sort_steps(arr):
    # Salin array asli agar data original tidak berubah selama visualisasi
    a = arr[:] #array utama yang diurutkan
    n = len(a)

    # Stack digunakan untuk simulasi, setiap elemen berisi pasangan (low,high) yang merupakan batas subarray yang perlu diurutkan
    stack = [(0, n - 1)]

    # Yield pertama: tampilkan kondisi awal array sebelum sorting dimulai
    # Format yield: (array, i, j, pivot_idx, swap_pair, pesan)
    yield a[:], None, None, None, None, "Mulai Quick Sort (Descending)"

    while stack:
        low, high = stack.pop() # Ambil batas subarray yang akan diproses dari stack

        if low >= high: # Jika subarray hanya 1 elemen atau kosong, lewati
            continue

        # ── MEDIAN OF THREE ───────────────────────────────────────────
        mid = (low + high) // 2 # Hitung index tengah subarray

        # Tampilkan 3 kandidat pivot: elemen paling kiri, tengah, kanan
        yield a[:], low, mid, high, None, (
            f"Kandidat pivot: "
            f"a[{low}]={a[low]}, a[{mid}]={a[mid]}, a[{high}]={a[high]}"
        )

        # Langkah 1: Membandingkan a[low] dan a[mid]
        # Jika a[low] lebih kecil, tukar agar yang lebih besar ada di kiri
        if a[low] < a[mid]:
            a[low], a[mid] = a[mid], a[low]
            yield a[:], low, mid, None, (low, mid), (
                f"Swap a[{low}] & a[{mid}] → "
                f"pastikan a[low] ≥ a[mid]"
            )

        # Langkah 2: Membandingkan a[low] dan a[high]
        # a[low] jadi yang terbesar dari ketiganya
        if a[low] < a[high]:
            a[low], a[high] = a[high], a[low]
            yield a[:], low, high, None, (low, high), (
                f"Swap a[{low}] & a[{high}] → "
                f"pastikan a[low] ≥ a[high]"
            )

        # Langkah 3: Membandingkan a[mid] dan a[high]
        # a[mid] jadi median dan a[high] adalah terkecil
        if a[mid] < a[high]:
            a[mid], a[high] = a[high], a[mid]
            yield a[:], mid, high, None, (mid, high), (
                f"Swap a[{mid}] & a[{high}] → "
                f"pastikan a[mid] ≥ a[high]"
            )

        # 3 langkah tersebut menghasilkan:
        # a[low]  = terbesar dari ketiganya
        # a[mid]  = median dari ketiganya (yang terpilih jadi pivot)
        # a[high] = terkecil dari ketiganya
        
        # Pindahkan median (a[mid]) ke posisi a[high] sebagai pivot
        a[mid], a[high] = a[high], a[mid]
        yield a[:], mid, high, None, (mid, high), (
            f"Pindah median ke a[{high}] → Pivot = {a[high]}"
        )
        
        # Pivot sekarang adalah median of three yang sudah dipindah ke posisi a[high]
        pivot = a[high]  # pivot: median of three yang sudah di posisi a[high]
        i = low - 1 # i: pointer batas zona besar yang dimulai sebelum low

        yield a[:], low, high, high, None, f"Pivot dipilih (Median): {pivot} (index {high})" #Tampilkan pivot final yang akan digunakan untuk partisi

        # PARTITION DESCENDING
        for j in range(low, high):  # j adalah pointer yang berjalan dari low sampai sebelum high
            yield a[:], i, j, high, None, f"Bandingkan a[{j}]={a[j]} dengan pivot={pivot}" #Tampilkan perbandingan elemen a[j] dengan pivot

            # jika a[j] lebih besar dari pivot pindahkan ke sisi kiri (zona besar)
            if a[j] > pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                yield a[:], i, j, high, (i, j), f"Swap a[{i}] dengan a[{j}]"

        # Setelah semua elemen diperiksa, pivot ditempatkan di posisi setelah semua elemen yang lebih besar
        a[i + 1], a[high] = a[high], a[i + 1]
        pivot_index = i + 1

        # Tampilkan posisi akhir pivot setelah partisi selesai
        yield a[:], pivot_index, None, pivot_index, (pivot_index, high), (
            f"Pivot dipindah ke index {pivot_index}"
        )

        # Masukkan dua subarray hasil partisi ke stack untuk diproses
        # Subarray kiri  : elemen dari low sampai sebelum pivot
        # Subarray kanan : elemen dari setelah pivot sampai high
        stack.append((low, pivot_index - 1))
        stack.append((pivot_index + 1, high))

    yield a[:], None, None, None, None, "Sorting selesai!"  # Semua subarray sudah selesai diproses, array terurut descending

#Konfirmasi SDA: 
# Mengapa pada code quick sort median of three saat mengurutkan jumlah data genap indeks yang dipilih sebagai median adalah yang dibulatkan kebawah? (dalam kasus pengurutan 10 data, kenapa bukan indeks 4 tetapi melainkan indeks 5?)
#   Tujuan median of three disini adalah mengambil satu elemen yang posisinya di sekitar tengah yang mana pada kasus ini, indeks 4 (bagian bawah/floor) dan 5 (bagian atas/ceiling)
#   memenuhi syarat tersebut. Akan tetapi, pada penerapannya di python, untuk pemilihan median atau yang menjadi nilai tengah adalah indeks 4 (hasil yang dibulatkan ke bawah).
#   Hal tersebut dikarenakan pada code ini digunakan operasi integer division (dalam code tanda "//" adalah integer division) yang mana hasil dari perhitungan untuk menentukan indeks sebagai "median" 
#   akan selalu dibulatan ke bawah. Sesuai dengan kasus saat algoritma mengurutkan data genap yakni 10, indeks yang menjadi median adalah indeks ke-4 yang didapat
#   dari perhitungan [mid = (low + high) // 2] = [(0+9) // 2] = 4,5 yang mana untuk hasilnnya kemudian dibulatkan ke bawah yaitu 4. (nilai indeks array tidak mungkin berbentuk float, jadi harus integer atau bulat)
#   Lalu, walaupun indeks 5 ini memenuhi syarat sebagai kandidat elemen yang posisinya ada di sekitar tengah, akan tetapi pemilihan indeks 5 tersebut berlawanan dengan konvensi universal integer arithmatic (aturan yang telah disepakati).
#   Selain itu, terdapat alasan matematikanya dimana ketika memilih indeks 5 (sebagai ceiling) maka hasil operasi sisa pembagiannya akan bernilai negatif, sedangkan ketika memilih
#   elemen di indeks low yakni 4 (floor) tetap memenuhi syarat/ operasi matematika dimana hasil sisa dari operasi pembagian selalu positif. 
# Sumber: 
# Rijaya, R., & Al Rivan, M. E. (2023). Perbandingan Penempatan Pivot Pada Quick Sort Berdasarkan Ukuran Pemusatan Data. Jurnal Algoritme, 4(1), 13–20. https://jurnal.mdp.ac.id/index.php/algoritme/article/view/5735    
# van Rossum, G. (2010, August 24). Why Python's integer division floors. The History of Python. https://python-history.blogspot.com/2010/08/why-pythons-integer-division-floors.html
# Codex, A. C. (2023, October 12). Quick sort algorithm in Python. Reintech. https://reintech.io/blog/mastering-quick-sort-algorithm-python
# Python Software Foundation. Glossary: Floor division. Python Documentation. https://docs.python.org/3/glossary.html#term-floor-division

# ── Kotak Angka ───────────────────────────────────────────────────────────────
class NumberBox(QFrame):
    def __init__(self, value):
        super().__init__()
        self.value = value

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(50, 50)

        self.number_size = 14
        self.role_size = 10

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        self.lbl_value = QLabel(str(value))
        self.lbl_value.setAlignment(Qt.AlignCenter)

        self.lbl_role = QLabel("")
        self.lbl_role.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.lbl_value)
        layout.addWidget(self.lbl_role)

        self.set_role()

    def set_value(self, value):
        self.value = value
        self.lbl_value.setText(str(value))

    def set_font_sizes(self, number_size, role_size):
        self.number_size = number_size
        self.role_size = role_size

    def set_role(self, role_text="", bg="#ffffff", border="#cccccc",
                 value_color="#333333", role_color="#666666"):

        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: 2px solid {border};
                border-radius: 14px;
            }}
        """)

        self.lbl_role.setText(role_text)

        self.lbl_value.setStyleSheet(
            f"font-size:{self.number_size}px; font-weight:bold; color:{value_color};"
        )
        self.lbl_role.setStyleSheet(
            f"font-size:{self.role_size}px; color:{role_color};"
        )

# ── Halaman Visualisasi Quick Sort ────────────────────────────────────────────
class QuickSortVisualizerPage(QWidget):
    def __init__(self):
        super().__init__()

        self.data_original = [] #list
        self.current_arr = []
        self.generator = None
        self.boxes = []

        self.max_cols = 10

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)

        main = QVBoxLayout(self)
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(10)

        # ── Judul ─────────────────────────────────────────────────────────────
        self.title = QLabel("VISUALISASI QUICK SORT (PIVOT MEDIAN OF TREE)")
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("font-size:20px; font-weight:bold; color:#1A3F8C;")
        main.addWidget(self.title)

        self.subtitle = QLabel("Biru = i, Kuning = j, Merah = Pivot, Hijau = Swap")
        self.subtitle.setStyleSheet("font-size:12px; color:#444;")
        main.addWidget(self.subtitle)

        # ── Status ────────────────────────────────────────────────────────────
        self.lbl_status = QLabel("Masukkan file excel, jalankan sorting.")
        self.lbl_status.setWordWrap(True)
        self.lbl_status.setStyleSheet("""
            font-size:13px;
            color:#333;
            background:white;
            padding:10px;
            border-radius:10px;
            border: 1px solid #DDD;
        """)
        main.addWidget(self.lbl_status)

        # ── Grid area ─────────────────────────────────────────────────────────
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)

        self.grid_layout.setAlignment(Qt.AlignCenter)

        self.grid_widget.setStyleSheet("""
            QWidget {
                background: #F8FAFF;
                border: 2px solid #D0D7FF;
                border-radius: 15px;
            }
        """)

        main.addWidget(self.grid_widget, stretch=10)

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_next = QPushButton("➡ Next Step")
        self.btn_next.clicked.connect(self.next_step)

        self.btn_play = QPushButton("▶ Auto Play")
        self.btn_play.clicked.connect(self.auto_play)

        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_pause.clicked.connect(self.pause_play)

        self.btn_reset = QPushButton("🔄 Reset")
        self.btn_reset.clicked.connect(self.reset)

        self.buttons = [self.btn_next, self.btn_play, self.btn_pause, self.btn_reset]

        for btn in self.buttons:
            btn.setMinimumHeight(40)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        btn_row.addWidget(self.btn_next)
        btn_row.addWidget(self.btn_play)
        btn_row.addWidget(self.btn_pause)
        btn_row.addWidget(self.btn_reset)

        main.addLayout(btn_row)

        self.lbl_status.setText("Silakan masukkan file Excel terlebih dahulu, lalu jalankan sorting.")

    # ── Resize event ──────────────────────────────────────────────────────────
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_layout()

    # ── Data dari main.py ─────────────────────────────────────────────────────
    def set_data(self, data):
        if len(data) > 40:
            self.lbl_status.setText("⚠️ Visualisasi hanya tersedia maksimal 40 data.")
            self.data_original = []
            return
        self.data_original = data
        self.reset()

    # ── Build kotak ───────────────────────────────────────────────────────────
    def build_boxes(self, arr):
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        self.boxes = []
        self.current_arr = arr[:]

        for idx, val in enumerate(arr):
            box = NumberBox(val)
            self.boxes.append(box)

            r = idx // self.max_cols
            c = idx % self.max_cols
            self.grid_layout.addWidget(box, r, c)

        self.update_responsive_layout()

    # ── Responsive updater ────────────────────────────────────────────────────
    def update_responsive_layout(self):
        if not self.boxes:
            return

        w = self.width()

        count = len(self.boxes)
        rows = (count + self.max_cols - 1) // self.max_cols

        grid_height = self.grid_widget.height()
        box_size_by_height = grid_height // max(1, rows + 1)

        box_size_by_width = self.width() // (self.max_cols + 2)

        box_size = min(box_size_by_width, box_size_by_height)

        box_size = max(50, min(110, box_size))

        number_font = max(11, int(box_size / 3.2))
        role_font = max(8, int(box_size / 6.5))

        for box in self.boxes:
            box.setMinimumSize(box_size, box_size)
            box.setMaximumSize(box_size, box_size)
            box.set_font_sizes(number_font, role_font)

        title_font = max(16, min(28, w // 45))
        subtitle_font = max(11, min(18, w // 80))
        status_font = max(11, min(16, w // 90))

        self.title.setStyleSheet(
            f"font-size:{title_font}px; font-weight:bold; color:#1A3F8C;"
        )
        self.subtitle.setStyleSheet(
            f"font-size:{subtitle_font}px; color:#444;"
        )
        self.lbl_status.setStyleSheet(f"""
            font-size:{status_font}px;
            color:#333;
            background:white;
            padding:10px;
            border-radius:10px;
            border: 1px solid #DDD;
        """)

        btn_font = max(10, min(18, w // 90))
        btn_height = max(40, min(65, int(box_size * 0.55)))

        for btn in self.buttons:
            btn.setMinimumHeight(btn_height)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: #1A3F8C;
                    color: white;
                    border-radius: 12px;
                    font-size: {btn_font}px;
                    font-weight: bold;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background: #2563EB;
                }}
            """)

        self.update_display(self.current_arr, None, None, None, None)

    # ── Reset sorting ─────────────────────────────────────────────────────────
    def reset(self):
        self.timer.stop()

        if not self.data_original:
            self.lbl_status.setText("⚠️ Data belum ada. Jalankan sorting dulu dari Dashboard.")
            return

        self.generator = quick_sort_steps(self.data_original)

        self.lbl_status.setText("Reset berhasil. Klik Next Step untuk mulai.")
        self.build_boxes(self.data_original)
        self.update_display(self.data_original, None, None, None, None)

    # ── Auto Play ─────────────────────────────────────────────────────────────
    def auto_play(self):
        self.timer.start(900)

    def pause_play(self):
        self.timer.stop()

    # ── Next Step ─────────────────────────────────────────────────────────────
    def next_step(self):
        if not self.generator:
            return

        try:
            arr, i, j, pivot_idx, swap_pair, msg = next(self.generator)
            self.lbl_status.setText(msg)

            self.current_arr = arr[:]

            if len(arr) == len(self.boxes):
                for idx, val in enumerate(arr):
                    self.boxes[idx].set_value(val)
            else:
                self.build_boxes(arr)

            self.update_display(arr, i, j, pivot_idx, swap_pair)

        except StopIteration:
            self.timer.stop()
            self.lbl_status.setText("Sorting selesai!")

    # ── Update display warna ──────────────────────────────────────────────────
    def update_display(self, arr, i, j, pivot_idx, swap_pair):
        for idx, box in enumerate(self.boxes):
            role = ""
            bg = "#FFFFFF"
            border = "#CCCCCC"
            value_color = "#333333"
            role_color = "#666666"

            # pivot
            if pivot_idx is not None and idx == pivot_idx:
                role = "pivot"
                bg = "#FFD6D6"
                border = "#DC2626"
                value_color = "#7F1D1D"
                role_color = "#7F1D1D"

            # i
            if i is not None and idx == i:
                role = "i"
                bg = "#D6E4FF"
                border = "#2563EB"
                value_color = "#1A3F8C"
                role_color = "#1A3F8C"

            # j
            if j is not None and idx == j:
                role = "j"
                bg = "#FFF4CC"
                border = "#F59E0B"
                value_color = "#8A4B00"
                role_color = "#8A4B00"

            # swap highlight
            if swap_pair is not None and idx in swap_pair:
                role = "swap"
                bg = "#D1FAE5"
                border = "#10B981"
                value_color = "#065F46"
                role_color = "#065F46"

            box.set_role(role, bg, border, value_color, role_color)