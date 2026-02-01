import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

API_UPLOAD = "http://localhost:8000/api/upload/"
API_PDF = "http://localhost:8000/api/report/"
API_KEY = "demo-intern-key-123"

COLORS = {
    "flowrate": "#0d6efd",
    "pressure": "#198754",
    "temperature": "#fd7e14",
}

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.resize(1100, 800)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.header()
        self.upload_button()   # ⬅️ like web app (top)
        self.kpis()
        self.charts()
        self.table()
        self.pdf_button()      # ⬅️ like web app (bottom)

    def header(self):
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("font-size:22px; font-weight:bold;")
        subtitle = QLabel("Analyze performance, trends, and safety parameters")
        subtitle.setStyleSheet("color: gray;")
        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

    # 🔘 Upload CSV (WEB-LIKE)
    def upload_button(self):
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        self.upload_btn.clicked.connect(self.upload)
        self.layout.addWidget(self.upload_btn)

    def kpis(self):
        self.kpi_row = QHBoxLayout()
        self.kpi_labels = []
        for name in ["Total", "Flowrate", "Pressure", "Temperature"]:
            lbl = QLabel("0")
            lbl.setStyleSheet("font-size:18px;")
            box = QVBoxLayout()
            box.addWidget(QLabel(name))
            box.addWidget(lbl)
            self.kpi_labels.append(lbl)
            self.kpi_row.addLayout(box)
        self.layout.addLayout(self.kpi_row)

    def charts(self):
        self.fig = Figure(figsize=(8, 4))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.layout.addWidget(self.canvas)

    def table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #eef2f7;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                padding: 8px;
                border-bottom: 1px solid #e2e8f0;
                font-weight: 600;
            }
        """)

        self.layout.addWidget(self.tableWidget)

    # 🔘 Download PDF (WEB-LIKE)
    def pdf_button(self):
        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #198754;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #157347;
            }
        """)
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.layout.addWidget(self.pdf_btn)

    def upload(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        with open(path, "rb") as f:
            res = requests.post(
                API_UPLOAD,
                files={"file": f},
                headers={"X-API-KEY": API_KEY}
            )

        data = res.json()
        s = data["summary"]

        self.kpi_labels[0].setText(str(s["total_equipment"]))
        self.kpi_labels[1].setText(f'{s["avg_flowrate"]:.2f}')
        self.kpi_labels[2].setText(f'{s["avg_pressure"]:.2f}')
        self.kpi_labels[3].setText(f'{s["avg_temperature"]:.2f}')

        self.render_charts(s)
        self.render_table(data["preview"])

    def render_charts(self, s):
        self.fig.clear()
        ax1 = self.fig.add_subplot(121)
        ax2 = self.fig.add_subplot(122)

        ax1.bar(
            ["Flowrate", "Pressure", "Temperature"],
            [s["avg_flowrate"], s["avg_pressure"], s["avg_temperature"]],
            color=list(COLORS.values())
        )

        ax2.pie(
            s["type_distribution"].values(),
            labels=s["type_distribution"].keys(),
            autopct="%1.0f%%"
        )

        self.canvas.draw()

    def render_table(self, rows):
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Equipment", "Type", "Flowrate", "Pressure", "Temperature"]
        )

        for i, r in enumerate(rows):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(r["EquipmentName"]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(r["Type"]))

            for col, key in enumerate(["Flowrate", "Pressure", "Temperature"], start=2):
                item = QTableWidgetItem(str(r[key]))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.tableWidget.setItem(i, col, item)

    def download_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf")
        if not path:
            return

        r = requests.get(
            API_PDF,
            headers={"X-API-KEY": API_KEY}
        )
        open(path, "wb").write(r.content)

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())


