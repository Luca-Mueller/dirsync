from dir_copy import DirSync
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DirSync")
        self.src_pth = None
        self.dst_pth = None
        self.ds = None

        # Src
        src_pth_input = QLineEdit()
        src_pth_input.setMaxLength(50)
        src_pth_input.setPlaceholderText("Enter your text")

        src_pth_input.returnPressed.connect(self.return_pressed)
        src_pth_input.selectionChanged.connect(self.selection_changed)
        src_pth_input.textChanged.connect(self.text_changed)
        src_pth_input.textEdited.connect(self.text_edited)

        # Dst
        dst_pth_input = QLineEdit()
        dst_pth_input.setMaxLength(50)
        dst_pth_input.setPlaceholderText("Enter your text")

        dst_pth_input.returnPressed.connect(self.return_pressed)
        dst_pth_input.selectionChanged.connect(self.selection_changed)
        dst_pth_input.textChanged.connect(self.text_changed)
        dst_pth_input.textEdited.connect(self.text_edited)

        # Layout
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        input_layout.addWidget(src_pth_input)
        input_layout.addWidget(dst_pth_input)
        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        main_layout.addWidget(input_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        #self.setCentralWidget(src_pth_input)
        #self.setCentralWidget(dst_pth_input)

    def return_pressed(self, input):
        print(type(input))

    def selection_changed(self):
        print("Selection Changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)

class Color(QWidget):
    def __init__(self, color: str):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()