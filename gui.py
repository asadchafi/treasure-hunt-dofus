import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QLabel
from PyQt5 import QtCore, QtGui

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('TreasureHunter')
        self.setGeometry(100, 100, 300, 600)  # Window size 300x600
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # Keep window always on top

        # Initialize the main layout (vertical layout for the whole window)
        main_layout = QVBoxLayout()

        # Create the coordinates label
        self.coordinates = QLabel('-6, -7', self)
        self.coordinates.setAlignment(QtCore.Qt.AlignCenter)  # Center align the label
        
        # Set the font size of the label to be bigger
        font = QtGui.QFont()
        font.setPointSize(20)  # Increase the font size
        self.coordinates.setFont(font)

        # Add the coordinates label to the main layout
        main_layout.addWidget(self.coordinates)

        # Create a box (group) for the buttons (two on top, two on bottom)
        button_box = QVBoxLayout()

        # Create 4 buttons (top-left, top-right, bottom-left, bottom-right)
        top_button = QPushButton('Top', self)
        right_button = QPushButton('Right', self)
        bottom_button = QPushButton('Bottom', self)
        left_button = QPushButton('Left', self)

        # Create a list widget (dummy data)
        self.list_widget = QListWidget(self)
        self.list_widget.addItems([f"Item {i}" for i in range(1, 11)])

        # Add buttons to the button box
        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        # Add buttons to respective rows
        top_row.addWidget(top_button)
        top_row.addWidget(right_button)

        bottom_row.addWidget(bottom_button)
        bottom_row.addWidget(left_button)

        # Add rows to the button box
        button_box.addLayout(top_row)
        button_box.addLayout(bottom_row)

        # Add the button box and the list widget to the main layout
        main_layout.addLayout(button_box)
        main_layout.addWidget(self.list_widget)

        # Set the main layout for the window
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
