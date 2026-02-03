import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QLineEdit, QStackedWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_BASE = "https://chemical-equipment-visualizer-i9my.onrender.com/api"


# ---------- CARD ----------
class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 16px;
            }
        """)


# ---------- MAIN WINDOW ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1200, 800)

        self.data = None
        self.history = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.build_navbar()
        self.build_stack()

    # ---------- NAVBAR ----------
    def build_navbar(self):
        nav_widget = QWidget()
        nav_widget.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #ff512f,
                stop:1 #f09819
            );
        """)

        nav = QHBoxLayout(nav_widget)
        nav.setContentsMargins(20, 10, 20, 10)

        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        upload_btn = QPushButton("Upload")
        history_btn = QPushButton("History")

        for btn in (upload_btn, history_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: white;
                    font-size: 14px;
                    border: none;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)

        upload_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        history_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        nav.addWidget(title)
        nav.addStretch()
        nav.addWidget(upload_btn)
        nav.addWidget(history_btn)

        self.main_layout.addWidget(nav_widget)

    # ---------- STACK ----------
    def build_stack(self):
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.stack.addWidget(self.upload_view())
        self.stack.addWidget(self.dashboard_view())
        self.stack.addWidget(self.history_view())

    # ---------- BUTTON STYLE ----------
    def style_orange_button(self, btn):
        btn.setStyleSheet("""
            QPushButton {
                background-color: #f09819;
                color: white;
                font-size: 13px;
                padding: 8px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff8c00;
            }
        """)

    # ---------- UPLOAD VIEW ----------
    def upload_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setContentsMargins(0, 40, 0, 0)

        card = Card()
        card.setFixedWidth(500)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        title = QLabel("Upload CSV File")
        title.setFont(QFont("Arial", 14, QFont.Bold))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Your Email")

        select_btn = QPushButton("Select CSV")
        upload_btn = QPushButton("Upload")

        self.style_orange_button(select_btn)
        self.style_orange_button(upload_btn)

        select_btn.clicked.connect(self.select_file)
        upload_btn.clicked.connect(self.upload_csv)

        card_layout.addWidget(title)
        card_layout.addWidget(self.name_input)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(select_btn)
        card_layout.addWidget(upload_btn)

        layout.addWidget(card)
        return widget

    # ---------- DASHBOARD ----------
    def dashboard_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Summary cards
        summary_row = QHBoxLayout()
        summary_row.setSpacing(16)

        self.total_card = self.create_summary_card("Total Equipment")
        self.flow_card = self.create_summary_card("Avg Flowrate")
        self.pressure_card = self.create_summary_card("Avg Pressure")
        self.temp_card = self.create_summary_card("Avg Temperature")

        summary_row.addWidget(self.total_card)
        summary_row.addWidget(self.flow_card)
        summary_row.addWidget(self.pressure_card)
        summary_row.addWidget(self.temp_card)

        layout.addLayout(summary_row)

        # Chart card
        chart_card = Card()
        chart_layout = QVBoxLayout(chart_card)

        chart_title = QLabel("Equipment Type Distribution")
        chart_title.setFont(QFont("Arial", 13, QFont.Bold))

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.canvas)

        layout.addWidget(chart_card)

        return widget

    # ---------- HISTORY ----------
    def history_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        card = Card()
        card_layout = QVBoxLayout(card)

        title = QLabel("Upload History")
        title.setFont(QFont("Arial", 14, QFont.Bold))

        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(
            ["Name", "Email", "Uploaded At", "Total Equipment"]
        )

        card_layout.addWidget(title)
        card_layout.addWidget(self.history_table)
        layout.addWidget(card)

        return widget

    # ---------- SUMMARY CARD ----------
    def create_summary_card(self, title):
        card = Card()
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 12px;")

        value_label = QLabel("0")
        value_label.setStyleSheet("""
            color: #111;
            font-size: 22px;
            font-weight: bold;
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.value_label = value_label
        return card

    # ---------- LOGIC ----------
    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if file:
            self.file_path = file

    def upload_csv(self):
        if not self.name_input.text() or not self.email_input.text():
            return
        if not hasattr(self, "file_path"):
            return

        with open(self.file_path, "rb") as f:
            response = requests.post(
                f"{API_BASE}/upload/",
                files={"file": f}
            )

        if response.status_code == 200:
            self.data = response.json()
            self.update_dashboard()

            self.history.append([
                self.name_input.text(),
                self.email_input.text(),
                "Now",
                str(self.data["total_count"])
            ])
            self.update_history()

            self.stack.setCurrentIndex(1)

    def update_dashboard(self):
        self.total_card.value_label.setText(str(self.data["total_count"]))
        self.flow_card.value_label.setText(f"{self.data['avg_flowrate']:.2f}")
        self.pressure_card.value_label.setText(f"{self.data['avg_pressure']:.2f}")
        self.temp_card.value_label.setText(f"{self.data['avg_temperature']:.2f}")

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(
            self.data["type_distribution"].keys(),
            self.data["type_distribution"].values(),
            color="#f09819"
        )
        self.canvas.draw()

    def update_history(self):
        self.history_table.setRowCount(len(self.history))
        for r, row in enumerate(self.history):
            for c, val in enumerate(row):
                self.history_table.setItem(r, c, QTableWidgetItem(val))


# ---------- RUN ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())