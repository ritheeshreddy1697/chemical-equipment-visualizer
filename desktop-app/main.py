import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = "http://127.0.0.1:8000/api/upload/"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 900, 700)

        self.layout = QVBoxLayout()

        # Upload button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_btn)

        # Summary
        self.summary_label = QLabel("")
        self.layout.addWidget(self.summary_label)

        # Table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

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
                QMessageBox.warning(
                    self, "Error", f"Upload failed ❌ (Status {response.status_code})"
                )
                return

            data = response.json()
            QMessageBox.information(self, "Success", "CSV uploaded successfully ✅")

            self.show_summary(data)
            self.show_table(data["table_data"])
            self.show_chart(data["type_distribution"])

        except Exception as e:
            QMessageBox.critical(self, "Exception", str(e))

    def show_summary(self, data):
        text = (
            f"Total Equipment: {data['total_count']}\n"
            f"Average Flowrate: {data['avg_flowrate']:.2f}\n"
            f"Average Pressure: {data['avg_pressure']:.2f}\n"
            f"Average Temperature: {data['avg_temperature']:.2f}"
        )
        self.summary_label.setText(text)

    def show_table(self, table_data):
        headers = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(table_data))
        self.table.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(table_data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row["Equipment Name"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row["Type"])))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row["Flowrate"])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row["Pressure"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["Temperature"])))

        self.table.resizeColumnsToContents()

    def show_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = list(distribution.keys())
        counts = list(distribution.values())

        ax.bar(types, counts)
        ax.set_title("Equipment Type Distribution")
        ax.set_xlabel("Equipment Type")
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=30)

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
