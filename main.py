import sys
import boto3
import os

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, \
    QDialog, QWidget, QTableWidgetItem, QTableWidget

# Define your AWS credentials and S3 bucket name
aws_access_key_id = 'dere'
aws_secret_access_key = 'boyu'
bucket_name = 'kavaklar'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

class CloudStorageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cloud Storage App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.content_panel = QTableWidget()
        self.content_panel.setColumnCount(1)  # One column for file names
        self.content_panel.setHorizontalHeaderLabels(["File Name"])
        self.layout.addWidget(self.content_panel)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.list_files)
        self.layout.addWidget(self.refresh_button)

        self.list_files()

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName()
        if file_path:
            file_name = QFileInfo(file_path).fileName()
            s3.upload_file(file_path, bucket_name, file_name)
            self.list_files()

    def list_files(self):
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            file_list = [obj['Key'] for obj in response['Contents']]
            self.update_content_panel(file_list)
        else:
            self.update_content_panel([])

    def update_content_panel(self, file_list):
        self.content_panel.setRowCount(len(file_list))
        for row, file_name in enumerate(file_list):
            item = QTableWidgetItem(file_name)
            self.content_panel.setItem(row, 0, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CloudStorageApp()
    window.show()
    sys.exit(app.exec_())

