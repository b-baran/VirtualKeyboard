import os

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtQml import *

# import virtual keyboard module 
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


# define custom QLineEdit widget
class custom_QLineEdit(QLineEdit):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()


# example of PySide2 application embedding a QML view
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # set title
        self.setWindowTitle("PySide2 - Simple Virtual Keyboard Handler")

        # set app size 
        self.resize(900, 600)

        # define custom widgets
        self.custom_QLineEdit = custom_QLineEdit()

        # define main widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.setLayout(self.layout)

        # define main frame
        self.mainFrame = QFrame(self.centralWidget)
        
        # define main frame layout
        self.mainFrameLayout = QVBoxLayout(self.mainFrame)
        self.mainFrame.setLayout(self.mainFrameLayout)  
        
        # define label of text input
        self.inuput_text_label = QLabel("Text Input:")
        self.mainFrameLayout.addWidget(self.inuput_text_label)

        # define custom widget for text input
        self.inuput_text_field = custom_QLineEdit()
        self.mainFrameLayout.addWidget(self.inuput_text_field)

        # define label of number input
        self.inuput_number_label = QLabel("Number Input:")
        self.mainFrameLayout.addWidget(self.inuput_number_label)

        # define custom widget for number input
        self.inuput_number_field = custom_QLineEdit()

        # define input method hints
        self.inuput_number_field.setInputMethodHints(Qt.ImhFormattedNumbersOnly)

        # attach custom widget to main frame
        self.mainFrameLayout.addWidget(self.inuput_number_field)

        # attach simple wiget to main frame
        self.simple_inuput_label = QLabel("Test button:")
        self.mainFrameLayout.addWidget(self.simple_inuput_label)

        # define simple widget 
        self.simple_button = QPushButton("Test Button")
        self.simple_button.setMaximumWidth(200)

        self.mainFrameLayout.addWidget(self.simple_button)

        # attach main frame to main widget
        self.layout.addWidget(self.mainFrame)

        # define keyboard frame
        self.keyboardFrame = QFrame(self.centralWidget)
        self.keyboardFrame.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        # define keyboard frame layout
        self.keyboardFramelayout = QVBoxLayout(self.keyboardFrame)
        self.keyboardFramelayout.setSpacing(0)
        self.keyboardFrame.setLayout(self.keyboardFramelayout)

        # create keyboard widget
        self.keyboard = QQuickWidget(self.keyboardFrame)
        self.keyboard.setMinimumSize(QSize(845, 320))
        self.keyboard.setSource(QUrl.fromLocalFile("src/keyboard.qml"))
        self.keyboard.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.keyboard.setAttribute(Qt.WA_AcceptTouchEvents)
        self.keyboard.setFocusPolicy(Qt.NoFocus)
        self.keyboard.setWindowFlags(Qt.FramelessWindowHint)
        self.keyboard.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # add widget to the layout
        self.keyboardFramelayout.addWidget(self.keyboard, 0, Qt.AlignCenter)

        # attach keyboard frame to main widget
        self.layout.addWidget(self.keyboardFrame)

        # create trigers for input fields
        self.inuput_text_field.focused.connect(self.open_keyboard_frame)
        self.inuput_text_field.noneFocused.connect(self.close_keyboard_frame)

        self.inuput_number_field.focused.connect(self.open_keyboard_frame)
        self.inuput_number_field.noneFocused.connect(self.close_keyboard_frame)


    def open_keyboard_frame(self):

        # logic to open keyboard frame
        if self.check_keyboard_visibility() and self.keyboardFrame.height() == 0:
            pass

        elif (not self.check_keyboard_visibility()) and self.keyboardFrame.height() != 0:
            QApplication.instance().inputMethod().show()

        elif (not self.check_keyboard_visibility()) and self.keyboardFrame.height() == 0:
            self.keyboard_frame_toggle(True)
            QApplication.instance().inputMethod().show()


    def close_keyboard_frame(self):

        virtual_keyboard = QApplication.instance().inputMethod()

        virtual_keyboard.hide()

        self.keyboard_frame_toggle(True)

    
    def check_keyboard_visibility(self):

        # get access to the virtual keyboard widget
        virtual_keyboard = QApplication.instance().inputMethod()

        # check if virtual keyboard is visible
        try:
            return virtual_keyboard.isVisible()
        
        except BaseException:
            raise Exception("Sorry, virtual keyboard is not accessible!")

    
    def keyboard_frame_toggle(self, enable):

        if enable:

            # get actual height
            height = self.keyboardFrame.height()
            heightContentBox = self.mainFrame.height()

            # define max and standard height
            maxExtend = 320
            standardExtend = 0

            # set max height
            if height == 0:
                heightExtend = maxExtend
            else:
                heightExtend = standardExtend

            self.keyboard_frame_animation(heightContentBox, height, heightExtend)


    def keyboard_frame_animation(self, content_box_height, keyboard_box_height, heightExtend):

            if keyboard_box_height == 0:
                keyboard_height = heightExtend
            else:
                keyboard_height = 0

            # animation keyboard box
            self.keyboard_box = QPropertyAnimation(self.keyboardFrame, b"maximumHeight")
            self.keyboard_box.setDuration(0)
            self.keyboard_box.setStartValue(keyboard_box_height)
            self.keyboard_box.setEndValue(keyboard_height)
            self.keyboard_box.setEasingCurve(QEasingCurve.InOutQuart)

            # run window animation
            self.group = QParallelAnimationGroup()
            self.group.addAnimation(self.keyboard_box)
            self.group.start()
            

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
