"""
    DirSync GUI
    Icons by Yusuke Kamiyamane (http://p.yusukekamiyamane.com/)
"""

from dir_copy import Select, DirSync
import sys
import pathlib

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, \
                            QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
                            QCheckBox, QToolBar, QAction
from PyQt5.QtGui import QColor, QPalette, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DirSync")
        self.setGeometry(700, 500, 300, 300)

        self.src_pth = pathlib.Path()
        self.dst_pth = pathlib.Path()
        self.ignore = list()
        self.selected = Select.ALL
        self.ds = None
        self.widgets = dict()

        self.setup()

    def setup(self):
        # Actions
        switch_action = QAction(QIcon("../../Fugue Icons/icons/arrow-switch.png"),
                                "Switch", self)
        switch_action.setStatusTip("Switch Source & Destination Path")
        switch_action.triggered.connect(self.switch)
        self.menuBar().addAction(switch_action)

        sync_action = QAction(QIcon("../../Fugue Icons/icons/drive--plus.png"), "Sync", self)
        sync_action.setStatusTip("Sync Directories")
        sync_action.triggered.connect(self.sync)
        self.menuBar().addAction(sync_action)

        # Src Input
        src_label = QLabel()
        src_label.setText("From:")
        src_pth_input = QLineEdit()
        src_pth_input.setMaxLength(100)
        src_pth_input.setPlaceholderText("Source Path")
        self.widgets["src_pth_input"] = src_pth_input

        src_pth_input.textEdited.connect(self.src_text_edited)

        # Dst Input
        dst_label = QLabel()
        dst_label.setText("To:")
        dst_pth_input = QLineEdit()
        dst_pth_input.setMaxLength(100)
        dst_pth_input.setPlaceholderText("Destination Path")
        self.widgets["dst_pth_input"] = dst_pth_input

        dst_pth_input.textEdited.connect(self.dst_text_edited)

        # Ignore Input
        ignore_label = QLabel()
        ignore_label.setText("Ignore:")
        ignore_input = QLineEdit()
        ignore_input.setMaxLength(200)
        ignore_input.setPlaceholderText("DirName, FileName, ...")
        self.widgets["ignore_input"] = ignore_input

        ignore_input.textChanged.connect(self.ignore_text_edited)

        # Switch button (switch src / dst)
        switch_button = QPushButton("Switch Paths")
        switch_button.addAction(switch_action)
        self.widgets["switch_button"] = switch_button

        # Sync Button
        sync_btn = QPushButton("Sync")
        sync_btn.addAction(sync_action)
        self.widgets["sync_btn"] = sync_btn

        # Checkoxes
        dir_checkbox = QCheckBox("Directories")
        dir_checkbox.setCheckState(Qt.Checked)
        self.widgets["dir_checkbox"] = dir_checkbox
        file_checkbox = QCheckBox("Files")
        file_checkbox.setCheckState(Qt.Checked)
        self.widgets["file_checkbox"] = file_checkbox

        dir_checkbox.stateChanged.connect(self.dir_state_changed)
        file_checkbox.stateChanged.connect(self.file_state_changed)

        # Layout
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        sync_layout = QVBoxLayout()
        checkbox_layout = QVBoxLayout()

        input_layout.addWidget(src_label)
        input_layout.addWidget(src_pth_input)
        input_layout.addWidget(dst_label)
        input_layout.addWidget(dst_pth_input)
        input_layout.addWidget(ignore_label)
        input_layout.addWidget(ignore_input)
        sync_layout.addWidget(switch_button)
        sync_layout.addWidget(sync_btn)
        checkbox_layout.addWidget(dir_checkbox)
        checkbox_layout.addWidget(file_checkbox)

        input_widget = Color("lightgreen")
        input_widget.setLayout(input_layout)
        sync_widget = Color("lightblue")
        sync_widget.setLayout(sync_layout)
        checkbox_widget = Color("lightblue")
        checkbox_widget.setLayout(checkbox_layout)
        buttons_widget = Color("darkcyan")
        buttons_widget.setLayout(buttons_layout)

        buttons_layout.addWidget(sync_widget)
        buttons_layout.addWidget(checkbox_widget)
        main_layout.addWidget(input_widget)
        main_layout.addWidget(buttons_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def src_text_edited(self, s):
        self.src_pth = pathlib.Path(s).resolve()

    def dst_text_edited(self, s):
        self.dst_pth = pathlib.Path(s).resolve()

    def ignore_text_edited(self, s):
        ignore = s.split(',')
        ignore = [i.strip() for i in ignore]
        self.ignore = ignore

    def dir_state_changed(self, state: int):
        if state == 0:
            self.selected = self.selected ^ Select.DIR
        else:
            self.selected = self.selected | Select.DIR

    def file_state_changed(self, state: int):
        if state == 0:
            self.selected = self.selected ^ Select.FILE
        else:
            self.selected = self.selected | Select.FILE

    def switch(self):
        self.src_pth, self.dst_pth = self.dst_pth, self.src_pth
        self.widgets["src_pth_input"].setText(str(self.src_pth))
        self.widgets["dst_pth_input"].setText(str(self.dst_pth))

    def sync(self):
        self.ds = None
        try:
            self.ds = DirSync(self.src_pth, self.dst_pth, selected=self.selected,
                              ignore=self.ignore, verbose=True)
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
app.setWindowIcon(QIcon("../../Fugue Icons/icons/arrow-circle-double-135.png"))

window = MainWindow()
window.show()

app.exec_()