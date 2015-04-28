from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QTreeWidget, QWidget)


__all__ = ['App']


class App(QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = MainWindow()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initContent()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SDR Scanner')
        self.resize(800, 600)
        self.center()
        self.show()

    def initContent(self):
        self.content = QWidget()
        self.setCentralWidget(self.content)

        waterfall = Waterfall(parent=self.content)
        freqlist = FreqList(parent=self.content)
        freq_control = FreqControl(parent=self.content)
        toggle_button = ToggleButton(parent=self.content)

        grid = QGridLayout()
        grid.addWidget(waterfall, 0, 0)
        grid.addWidget(freqlist, 0, 1)
        grid.addWidget(freq_control, 1, 0)
        grid.addWidget(toggle_button, 1, 1)

        self.content.setLayout(grid)

    def center(self):
        frameGm = self.frameGeometry()
        c = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(c)
        self.move(frameGm.topLeft())


class Waterfall(QWidget):
    pass


class FreqList(QTreeWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHeaderLabels(['Frequency', 'dbFS'])


class FreqControl(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        f_label = QLabel('Frequency:')
        f_input = QLineEdit()
        hz_label = QLabel('Hz')

        hbox = QHBoxLayout()
        hbox.addWidget(f_label)
        hbox.addWidget(f_input)
        hbox.addWidget(hz_label)
        self.setLayout(hbox)


class ToggleButton(QPushButton):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('text', 'Toggle')
        super().__init__(*args, **kwargs)
