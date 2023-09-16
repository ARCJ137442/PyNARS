import sys
from PySide6 import QtWidgets
# from PySide6
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout
from PySide6.QtWidgets import QFrame, QTextEdit, QToolBar, QPushButton, QSlider, QSplitter
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QScreen, QAction, QIcon, QColor, QFont, QKeyEvent, QFontDatabase
from qt_material import apply_stylesheet
import qtawesome as qta
from .utils import change_stylesheet
from .Widgets.Button import Button
from .Widgets.Slider import Slider

# create the application and the main window
class NARSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_layout()

    def init_layout(self):
        '''
        initialize the layout
        '''
        self.setGeometry(0, 0, 1000, 618)
        self._center_window()
        self.setWindowTitle('Open-NARS 4.0.0 (PyNARS)')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # create left area
        left_widget = QFrame(self)
        left_widget.setFixedWidth(200)
        self.left_layout = QVBoxLayout(left_widget)  # vertical layout

        # create right-top and right-bottom areas
        right_top_widget = QFrame(self)
        right_top_widget.setContentsMargins(0, 0, 0, 0)
        self.right_top_layout = QVBoxLayout(
            right_top_widget)  # vertical layout
        self.right_top_layout.setContentsMargins(0, 0, 0, 0)
        self.right_top_layout.setSpacing(0)
        
        right_bottom_widget = QFrame(self)
        right_bottom_widget.setContentsMargins(0, 0, 0, 0)
        self.right_bottom_layout = QVBoxLayout(
            right_bottom_widget)  # vertical layout
        self.right_bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.right_bottom_layout.setSpacing(0)

        # create a splitter to adjust the right two areas
        right_splitter = QSplitter(self)
        right_splitter.setOrientation(Qt.Vertical)  # vertical layout

        # add the widgets into the splitter
        right_splitter.addWidget(right_top_widget)
        right_splitter.addWidget(right_bottom_widget)
        right_splitter.setSizes([500, 120])

        # create main layout, and add the left widget and the right splitter into it
        main_layout = QHBoxLayout(central_widget)  # 水平布局
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_splitter)  # 添加可调整大小的右侧区域

        self.init_output_toolbar()
        self.init_output_textbox()
        self.init_input_textbox()

        self.slider_fontsize.value_changed_connect(
            lambda value: (change_stylesheet(self.text_output, f"font-size: {value+6}px;"), change_stylesheet(self.text_input, f"font-size: {value+6}px;")))
            
        self.button_clear.clicked.connect(
            lambda *args: self.text_output.clear())

    def init_output_toolbar(self):
        ''''''
        # tools bar
        toolbar = QWidget(self)
        toolbar.setFixedHeight(35)
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(3, 0, 3, 0)

        self.right_top_layout.addWidget(toolbar)
        
        # create buttons
        # run "qta-browser" to browse all the icons
        icon_clear = qta.icon('ph.file', color=QColor('white'))
        button_clear = Button(icon_clear)
        toolbar_layout.addWidget(button_clear)
        self.button_clear = button_clear

        icon_save = qta.icon('ph.floppy-disk', color=QColor('white'))
        button_save = Button(icon_save)
        toolbar_layout.addWidget(button_save)
        self.button_save = button_save

        slider_fontsize = Slider(Qt.Horizontal, 6, 40, 12, " Font size: ")
        slider_fontsize.setFixedWidth(100)
        toolbar_layout.addWidget(slider_fontsize)

        # set stretch and spacing 
        toolbar_layout.addStretch(1)
        toolbar_layout.setSpacing(3)

        self.slider_fontsize = slider_fontsize
    

    def init_output_textbox(self):
        ''''''
        # textbox of output
        text_output = QTextEdit(self)
        self.right_top_layout.addWidget(text_output)
        text_output.setReadOnly(True)
        # text = '\n'.join([f"This is line {i}" for i in range(50)])
        # text_output.setPlainText(text)
        text_output.setStyleSheet("font-family: Consolas, Monaco, Courier New; color: white;")
        
        def output_clicked(text_output: QTextEdit):
            print("line:", text_output.textCursor().blockNumber())
        text_output.mouseDoubleClickEvent = lambda x: output_clicked(
            text_output)
        self.text_output = text_output

    def init_input_textbox(self):
        ''''''
        text_input = QTextEdit(self)
        self.right_bottom_layout.addWidget(text_input)
        text_input.setReadOnly(False)
        text_input.setStyleSheet("font-family: Consolas, Monaco, Courier New; color: white;")
        text_input.installEventFilter(self)
        self.text_input = text_input
    
    def eventFilter(self, obj, event):
        '''
        For the input textbox, when pressing Enter, the content should be input to NARS reasoner; but when pressing shift+Enter, just start a new line.
        '''
        if obj == self.text_input and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                if event.modifiers() == Qt.ShiftModifier: # pressing Shift+Enter
                    return super().eventFilter(obj, event)
                else: # pressing Enter
                    self.input_narsese()
                    return True
        return super().eventFilter(obj, event)
    
    def input_narsese(self):
        content: str = self.text_input.toPlainText()
        self.text_input.clear()
        print(content)

    def _center_window(self):
        '''
        Move the window to the center of the screen
        '''
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())



