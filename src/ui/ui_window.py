import os.path
import sys

from PyQt5.QtCore import QRect, Qt, QResource
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout, QRadioButton, QPushButton, \
    QGroupBox, QApplication

from src.qr.qr_generator import create_qr_code_image

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'uee.wifiqrcreator.0.0.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.window_layout()
        self.ui_events()

    def setup_window(self):
        self.title = "Wi-Fi QR Generator"
        self.width = 640
        self.height = 840
        self.icon = "images/qr-code.png"

        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(self.title)

    def window_layout(self):
        # Setup Main Page
        self.centerWidget = QWidget(self)
        self.centerWidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QWidget(self.centerWidget)
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 621, 231))

        # Crate GridLayout
        self.glOptions = QGridLayout(self.gridLayoutWidget)

        # Create SSID Label
        self.lbSSID = QLabel(self.gridLayoutWidget)
        self.glOptions.addWidget(self.lbSSID, 1, 0, 1, 1)

        # Create SSID Hidden Checkbox
        self.chbIsHidden = QCheckBox(self.gridLayoutWidget)
        self.glOptions.addWidget(self.chbIsHidden, 2, 0, 1, 1)
        self.chbIsHidden.setChecked(True)

        # Create SSID Textbox
        self.tbSSID = QLineEdit(self.gridLayoutWidget)
        self.glOptions.addWidget(self.tbSSID, 3, 0, 1, 1)

        # Create Password Label
        self.lbPassword = QLabel(self.gridLayoutWidget)
        self.glOptions.addWidget(self.lbPassword, 5, 0, 1, 1)

        # Create Has Password Checkbox
        self.chbHasPassword = QCheckBox(self.gridLayoutWidget)
        self.chbHasPassword.setChecked(True)
        self.glOptions.addWidget(self.chbHasPassword, 6, 0, 1, 1)

        # Create Password Textbox
        self.tbPassword = QLineEdit(self.gridLayoutWidget)
        self.glOptions.addWidget(self.tbPassword, 7, 0, 1, 1)

        # Create Authentication Label
        self.lbAuthentication = QLabel(self.gridLayoutWidget)
        self.glOptions.addWidget(self.lbAuthentication, 8, 0, 1, 1)

        # Create Horizontal Layout
        self.hlAuthentication = QHBoxLayout()
        self.glOptions.addLayout(self.hlAuthentication, 9, 0, 1, 1)

        # Create WPA Radio Button
        self.rbWPA = QRadioButton(self.gridLayoutWidget)
        self.rbWPA.setChecked(True)
        self.hlAuthentication.addWidget(self.rbWPA)

        # Create WEP Radio Button
        self.rbWEP = QRadioButton(self.gridLayoutWidget)
        self.hlAuthentication.addWidget(self.rbWEP)

        # Create QR Code Button
        self.btnCreate = QPushButton(self.gridLayoutWidget)
        self.glOptions.addWidget(self.btnCreate, 10, 0, 1, 1)

        # Create Groupbox
        self.gbQRCode = QGroupBox(self.centerWidget)
        self.gbQRCode.setGeometry(QRect(40, 250, 564, 571))
        self.gbQRCode.setAlignment(Qt.AlignCenter)

        # Create QR Code Image
        self.image = QLabel(self.gbQRCode)
        self.image.setGeometry(QRect(8, 20, 544, 544))
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setScaledContents(True)

        # Set Central Widget
        self.setCentralWidget(self.centerWidget)

        # Set Text of UI Elements
        self.lbAuthentication.setText("Wi-Fi Authentication")
        self.lbSSID.setText("Wi-Fi SSID")
        self.chbIsHidden.setText("Is SSID Hidden?")
        self.lbPassword.setText("Wi-Fi Password")
        self.chbHasPassword.setText("Has Password?")
        self.rbWEP.setText("WEP")
        self.rbWPA.setText("WPA")
        self.btnCreate.setText("PushButton")
        self.gbQRCode.setTitle("QR Code")
        self.btnCreate.setText("Create QR Code")

    def ui_events(self):
        self.chbHasPassword.toggled.connect(lambda: self.on_chb_has_password(self.chbHasPassword.isChecked()))
        self.btnCreate.clicked.connect(lambda: self.on_btn_create_qr_code(self.tbSSID.text(), self.tbPassword.text()))

    def on_chb_has_password(self, is_checked: bool):
        self.tbPassword.setEnabled(is_checked)
        self.rbWPA.setEnabled(is_checked)
        self.rbWEP.setEnabled(is_checked)

    def on_btn_create_qr_code(self, ssid="", password=""):
        authentication = "nopass" if not self.chbHasPassword.isChecked() else "WPA" if self.rbWPA.isChecked() else "WEP"
        if authentication == "nopass":
            password = None

        print(f"Wi-Fi SSID: {ssid}")
        print(f"Wi-Fi SSID Hidden: {self.chbIsHidden.isChecked()}")
        print(f"Wi-Fi Authentication Mode: {authentication}")
        print(f"Wi-Fi Password: {password}")
        qr_image = create_qr_code_image(ssid,
                                        self.chbIsHidden.isChecked(),
                                        authentication,
                                        password)
        path = os.path.join(os.curdir, "QR-Images")
        if not os.path.exists(path):
            os.makedirs(path)
        image_path = os.path.join(path, f"{ssid}.png")
        print(f"Image Filename: {image_path}")
        qr_image.save(image_path, "png")
        self.image.setPixmap(QPixmap(image_path))


def main():
    app = QApplication(sys.argv)
    print(os.path.join(os.getcwd(), "icons", "qr-code.ico"))
    app.setWindowIcon(QIcon(os.path.join(os.getcwd(), "icons", "qr-code.ico")))
    window = MainWindow()
    window.show()
    app.exec()
