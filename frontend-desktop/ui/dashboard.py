from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QTableWidget, QTableWidgetItem, 
                             QListWidget, QSplitter, QMessageBox, QTabWidget,
                             QHeaderView)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from .api_client import APIClient

class Dashboard(QWidget):
    def __init__(self, api_client=None):
        super().__init__()
        self.api = api_client if api_client else APIClient()
        self.current_upload_id = None
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Sidebar
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_history_item)
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.refresh_history)
        
        sidebar = QVBoxLayout()
        sidebar.addWidget(QLabel("<b>Upload History</b>"))
        sidebar.addWidget(self.history_list)
        sidebar.addWidget(refresh_btn)
        sidebar.addStretch()
        
        # Content
        content_layout = QVBoxLayout()
        
        top_bar = QHBoxLayout()
        self.upload_btn = QPushButton("Upload New CSV")
        self.upload_btn.clicked.connect(self.upload_file)
        top_bar.addWidget(QLabel("Chemical Equipment Visualizer"))
        top_bar.addStretch()
        top_bar.addWidget(self.upload_btn)
        
        content_layout.addLayout(top_bar)
        
        self.tabs = QTabWidget()
        
        # Tab 1: Summary
        self.stats_label = QLabel("Please upload or select a dataset.")
        self.stats_label.setAlignment(Qt.AlignTop)
        self.stats_label.setStyleSheet("font-size: 14px; padding: 20px;")
        self.tabs.addTab(self.stats_label, "Summary Stats")
        
        # Tab 2: Charts
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.tabs.addTab(self.canvas, "Visualizations")
        
        # Tab 3: Data
        self.table = QTableWidget()
        self.tabs.addTab(self.table, "Raw Data")
        
        content_layout.addWidget(self.tabs)
        
        # Splitter to resize sidebar
        splitter = QSplitter(Qt.Horizontal)
        
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(content_widget)
        splitter.setSizes([200, 800])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
        self.refresh_history()

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '.', "CSV files (*.csv)")
        if fname:
            data, status = self.api.upload_csv(fname)
            if status == 201:
                self.current_upload_id = data['id']
                QMessageBox.information(self, "Success", "File uploaded successfully!")
                self.refresh_history()
                self.update_view()
            else:
                QMessageBox.critical(self, "Error", f"Upload failed: {data.get('error', 'Unknown')}")

    def refresh_history(self):
        history = self.api.get_history()
        self.history_list.clear()
        for item in history:
            text = f"ID: {item['id']} - {item['uploaded_at'].split('T')[0]}"
            list_item = QListWidget() # Wrong usage, it's addItem
            self.history_list.addItem(text)
            # Store ID in user role if needed, or parse text
            
    def load_history_item(self, item):
        text = item.text()
        try:
            # parsing "ID: <id> - ..."
            upload_id = int(text.split('-')[0].replace("ID:", "").strip())
            self.current_upload_id = upload_id
            self.update_view()
        except:
            pass

    def update_view(self):
        if not self.current_upload_id:
            return
            
        # 1. Summary
        summary = self.api.get_summary(self.current_upload_id)
        if summary:
            avgs = summary['averages']
            txt = (f"<b>Total Equipment Count:</b> {summary['total_count']}<br><br>"
                   f"<b>Average Flowrate:</b> {avgs['flowrate']}<br>"
                   f"<b>Average Pressure:</b> {avgs['pressure']}<br>"
                   f"<b>Average Temperature:</b> {avgs['temperature']}")
            self.stats_label.setText(txt)
            
            # 2. Charts
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            dist = summary['type_distribution']
            labels = [d['equipment_type'] for d in dist]
            values = [d['count'] for d in dist]
            ax.bar(labels, values, color='skyblue')
            ax.set_title("Equipment Type Distribution")
            ax.set_ylabel("Count")
            self.canvas.draw()
            
        # 3. Table
        detail = self.api.get_upload_detail(self.current_upload_id)
        if detail and 'equipments' in detail:
            eqs = detail['equipments']
            self.table.setRowCount(len(eqs))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["Name", "Type", "Flowrate", "Pressure", "Temp"])
            
            for i, eq in enumerate(eqs):
                self.table.setItem(i, 0, QTableWidgetItem(str(eq['equipment_name'])))
                self.table.setItem(i, 1, QTableWidgetItem(str(eq['equipment_type'])))
                self.table.setItem(i, 2, QTableWidgetItem(str(eq['flowrate'])))
                self.table.setItem(i, 3, QTableWidgetItem(str(eq['pressure'])))
                self.table.setItem(i, 4, QTableWidgetItem(str(eq['temperature'])))
