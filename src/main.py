import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class FramePredictorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Frame Predictor")
        self.setGeometry(100, 100, 400, 200)

        self.select_input_dir_button = QPushButton("Select input folder", self)
        self.select_input_dir_button.setGeometry(50, 50, 150, 30)
        self.select_input_dir_button.clicked.connect(self.select_directory)
        
        self.select_output_dir_button = QPushButton("Select output folder", self)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(220, 50, 100, 30)
        self.clear_button.clicked.connect(self.clear_selection)

        self.selected_directory = None

    def select_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.ReadOnly

        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            self.selected_directory = directory
            self.statusBar().showMessage(f"Selected Directory: {directory}")

    def clear_selection(self):
        self.selected_directory = None
        self.statusBar().clearMessage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FramePredictorApp()
    window.show()
    sys.exit(app.exec_())