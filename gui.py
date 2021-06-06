from dir_copy import DirSync
import sys
import pathlib

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, \
                            QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DirSync")
        self.setGeometry(700, 500, 300, 300)

        self.src_pth = pathlib.Path()
        self.dst_pth = pathlib.Path()
        self.ignore = list()
        self.ds = None
        self.widgets = dict()

        self.setup()

    def setup(self):
        # Src Input
        src_label = QLabel()
        src_label.setText("From:")
        src_pth_input = QLineEdit()
        src_pth_input.setMaxLength(100)
        src_pth_input.setPlaceholderText("Source Path")
        self.widgets["src_pth_input"] = src_pth_input

        src_pth_input.returnPressed.connect(self.src_return_pressed)
        src_pth_input.selectionChanged.connect(self.src_selection_changed)
        src_pth_input.textChanged.connect(self.src_text_changed)
        src_pth_input.textEdited.connect(self.src_text_edited)

        # Dst Input
        dst_label = QLabel()
        dst_label.setText("To:")
        dst_pth_input = QLineEdit()
        dst_pth_input.setMaxLength(100)
        dst_pth_input.setPlaceholderText("Destination Path")
        self.widgets["dst_pth_input"] = dst_pth_input

        dst_pth_input.returnPressed.connect(self.dst_return_pressed)
        dst_pth_input.selectionChanged.connect(self.dst_selection_changed)
        dst_pth_input.textChanged.connect(self.dst_text_changed)
        dst_pth_input.textEdited.connect(self.dst_text_edited)

        # Ignore Input
        ignore_label = QLabel()
        ignore_label.setText("Ignore:")
        ignore_input = QLineEdit()
        ignore_input.setMaxLength(200)
        ignore_input.setPlaceholderText("DirName, FileName, ...")
        self.widgets["ignore_input"] = ignore_input

        ignore_input.textChanged.connect(self.ignore_text_changed)

        # Switch button (switch src / dst)
        switch_button = QPushButton("Switch")
        switch_button.clicked.connect(self.switch)
        self.widgets["switch_button"] = switch_button

        # Sync Button
        sync_btn = QPushButton("Sync")
        sync_btn.clicked.connect(self.sync)
        self.widgets["sync_btn"] = sync_btn

        # Layout
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        sync_layout = QHBoxLayout()

        input_layout.addWidget(src_label)
        input_layout.addWidget(src_pth_input)
        input_layout.addWidget(dst_label)
        input_layout.addWidget(dst_pth_input)
        input_layout.addWidget(ignore_label)
        input_layout.addWidget(ignore_input)

        sync_layout.addWidget(switch_button)
        sync_layout.addWidget(sync_btn)

        input_widget = Color("lightgreen")
        input_widget.setLayout(input_layout)
        sync_widget = Color("darkcyan")
        sync_widget.setLayout(sync_layout)

        main_layout.addWidget(input_widget)
        main_layout.addWidget(sync_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def src_return_pressed(self):
        pass

    def src_selection_changed(self):
        pass

    def src_text_edited(self, s):
        pass

    def src_text_changed(self, s):
        self.src_pth = pathlib.Path(s).resolve()

    def dst_return_pressed(self):
        pass

    def dst_selection_changed(self):
        pass

    def dst_text_edited(self, s):
        pass

    def dst_text_changed(self, s):
        self.dst_pth = pathlib.Path(s).resolve()

    def ignore_text_changed(self, s):
        ignore = s.split(',')
        ignore = [i.strip() for i in ignore]
        self.ignore = ignore

    def switch(self):
        self.src_pth, self.dst_pth = self.dst_pth, self.src_pth
        self.widgets["src_pth_input"].setText(str(self.src_pth))
        self.widgets["dst_pth_input"].setText(str(self.dst_pth))

    def sync(self):
        self.ds = None
        try:
            self.ds = DirSync(self.src_pth, self.dst_pth, ignore=self.ignore, verbose=True)
            sys.stderr.write("Synchronizing " + str(self.src_pth) +
                             " with " + str(self.dst_pth) + '\n')
            self.ds.sync()
        except AssertionError as e:
            sys.stderr.write("Error while creating DS: " + str(e) + '\n')
            return


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