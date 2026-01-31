import sys
import requests

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_URL = "http://127.0.0.1:8000/api/upload/"


# ---------------- SUMMARY CARD ----------------
class InfoCard(QFrame):
    def __init__(self, title, value):
        super().__init__()

        self.setFixedSize(220, 110)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(str(value))
        value_label.setFont(QFont("Arial", 20, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        self.setLayout(layout)


# ---------------- MAIN WINDOW ----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Parameter Visualizer (Desktop)")
        self.setGeometry(100, 100, 1100, 780)

        # Dark dashboard background
        self.setStyleSheet("background-color: #121212;")

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(18)

        # -------- TITLE --------
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")

        title_container = QFrame()
        title_container.setStyleSheet("""
            background-color: #1f1f1f;
            padding: 18px;
            border-radius: 10px;
        """)

        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_container.setLayout(title_layout)
        self.main_layout.addWidget(title_container)

        # -------- UPLOAD --------
        upload_frame = QFrame()
        upload_frame.setStyleSheet("""
            background-color: #1f1f1f;
            padding: 12px;
            border-radius: 10px;
        """)

        upload_layout = QHBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setFixedSize(160, 40)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e86de;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1b4f72;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_csv)

        upload_layout.addStretch()
        upload_layout.addWidget(self.upload_btn)
        upload_layout.addStretch()

        upload_frame.setLayout(upload_layout)
        self.main_layout.addWidget(upload_frame)

        # -------- SUMMARY CARDS --------
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(20)
        self.cards_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(self.cards_layout)

        # -------- TABLE --------
        self.table = QTableWidget()
        self.table.setMinimumHeight(260)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                border-radius: 10px;
                gridline-color: #dcdcdc;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QHeaderView::section {
                background-color: #2e86de;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.table)

        # -------- CHART --------
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
        """)

        chart_layout = QVBoxLayout()
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        chart_frame.setLayout(chart_layout)

        self.main_layout.addWidget(chart_frame)

        self.setLayout(self.main_layout)

    # ---------------- CSV UPLOAD ----------------
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                response = requests.post(API_URL, files={"file": f})

            if response.status_code != 200:
                QMessageBox.warning(self, "Error", "Upload failed ❌")
                return

            data = response.json()
            QMessageBox.information(self, "Success", "CSV uploaded successfully ✅")

            self.show_cards(data)
            self.show_table(data["table_data"])
            self.show_chart(data["type_distribution"])

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ---------------- SUMMARY ----------------
    def show_cards(self, data):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cards = [
            ("Total Equipment", data["total_count"]),
            ("Avg Flowrate", f"{data['avg_flowrate']:.2f}"),
            ("Avg Pressure", f"{data['avg_pressure']:.2f}"),
            ("Avg Temperature", f"{data['avg_temperature']:.2f}")
        ]

        for title, value in cards:
            self.cards_layout.addWidget(InfoCard(title, value))

    # ---------------- TABLE ----------------
    def show_table(self, table_data):
        headers = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(table_data))
        self.table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(table_data):
            for c, key in enumerate(headers):
                item = QTableWidgetItem(str(row[key]))
                item.setForeground(Qt.black)  # FORCE VISIBILITY
                self.table.setItem(r, c, item)

        self.table.resizeColumnsToContents()

    # ---------------- CHART ----------------
    def show_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.bar(distribution.keys(), distribution.values())
        ax.set_title("Equipment Type Distribution")
        ax.set_xlabel("Equipment Type")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=25)

        self.canvas.draw()


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
