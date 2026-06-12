from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QGridLayout, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer


# ── Generator Selection Sort Step-by-Step ─────────────────────────────────────
def selection_sort_steps(arr):
    # Salin array asli agar data original tidak berubah selama visualisasi
    a = arr[:]
    n = len(a)

    # Iterasi luar: setiap putaran menempatkan satu elemen terbesar ke posisi i
    for i in range(n):
        max_idx = i # Asumsikan elemen terbesar sementara ada di posisi i
        yield a[:], i, max_idx, None, "Mulai iterasi, set max = i"  # Tampilkan awal iterasi dan posisi max sementara

        # Iterasi dalam: cari elemen terbesar di subarray a[i+1 .. n-1]
        for j in range(i + 1, n):
            yield a[:], i, max_idx, j, f"Bandingkan a[{j}] dengan a[{max_idx}]" # Tampilkan perbandingan a[j] dengan elemen max saat ini

            if a[j] > a[max_idx]:
                max_idx = j # Perbarui posisi max jika ditemukan elemen yang lebih besar
                yield a[:], i, max_idx, j, f"Nilai max baru ditemukan di index {max_idx}"

        # Setelah seluruh subarray diperiksa, tempatkan elemen terbesar ke posisi i
        if max_idx != i:
            a[i], a[max_idx] = a[max_idx], a[i] #Tukar elemen terbesar ke posisi i
            yield a[:], i, max_idx, None, f"Swap a[{i}] dengan a[{max_idx}]"
        else:   
            yield a[:], i, max_idx, None, f"Tidak ada swap, a[{i}] sudah minimum"   # a[i] sudah merupakan elemen terbesar di subarray, tidak perlu swap

    yield a[:], None, None, None, "Sorting selesai!"    # Semua elemen sudah berada di posisi yang benar, array terurut descending


# ── Kotak Angka (Responsive & Stable Font) ────────────────────────────────────
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

# ── Halaman Visualisasi Sorting ───────────────────────────────────────────────
class SortingVisualizerPage(QWidget):
    def __init__(self):
        super().__init__()

        self.data_original = []
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
        self.title = QLabel("VISUALISASI SELECTION SORT (DESCENDING)")
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("font-size:20px; font-weight:bold; color:#1A3F8C;")
        main.addWidget(self.title)

        self.subtitle = QLabel("Biru = i, Kuning = j, Hijau = Max")
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

        # default data kalau user belum upload
        self.data_original = []
        self.lbl_status.setText("Silakan masukkan file Excel terlebih dahulu, lalu jalankan sorting.")
        
    # ── Responsif resize ──────────────────────────────────────────────────────
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

    # ── Build kotak (sekali saja) ─────────────────────────────────────────────
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

        # box size responsive
        count = len(self.boxes)
        rows = (count + self.max_cols - 1) // self.max_cols

        grid_height = self.grid_widget.height()
        box_size_by_height = grid_height // max(1, rows + 1)

        box_size_by_width = self.width() // (self.max_cols + 2)

        box_size = min(box_size_by_width, box_size_by_height)

        # batasi supaya tidak terlalu besar
        box_size = max(50, min(110, box_size))

        # font size responsive (proporsional)
        number_font = max(11, int(box_size / 3.2))
        role_font = max(8, int(box_size / 6.5))

        for box in self.boxes:
            box.setMinimumSize(box_size, box_size)
            box.setMaximumSize(box_size, box_size)
            box.set_font_sizes(number_font, role_font)

        # title / subtitle responsive
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

        # button responsive
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

        # refresh role coloring supaya font-size kepakai terus
        self.update_display(self.current_arr, None, None, None)

    # ── Reset sorting ─────────────────────────────────────────────────────────
    def reset(self):
        self.timer.stop()

        if not self.data_original:
            self.lbl_status.setText("⚠️ Data belum ada. Jalankan sorting dulu dari Dashboard.")
            return
        
        self.generator = selection_sort_steps(self.data_original)

        self.lbl_status.setText("Reset berhasil. Klik Next Step untuk mulai.")
        self.build_boxes(self.data_original)
        self.update_display(self.data_original, None, None, None)

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
            arr, i, max_idx, j, msg = next(self.generator)
            self.lbl_status.setText(msg)

            self.current_arr = arr[:]

            # update value box tanpa rebuild
            if len(arr) == len(self.boxes):
                for idx, val in enumerate(arr):
                    self.boxes[idx].set_value(val)
            else:
                self.build_boxes(arr)

            self.update_display(arr, i, max_idx, j)

        except StopIteration:
            self.timer.stop()
            self.lbl_status.setText("Sorting selesai!")

    # ── Update warna pointer i/j/max ──────────────────────────────────────────
    def update_display(self, arr, i, max_idx, j):
        for idx, box in enumerate(self.boxes):
            role = ""
            bg = "#FFFFFF"
            border = "#CCCCCC"
            value_color = "#333333"
            role_color = "#666666"

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

            # max_idx (prioritas tertinggi)
            if max_idx is not None and idx == max_idx:
                role = "max"
                bg = "#D1FAE5"
                border = "#10B981"
                value_color = "#065F46"
                role_color = "#065F46"

            box.set_role(role, bg, border, value_color, role_color)