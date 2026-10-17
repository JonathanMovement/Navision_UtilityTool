import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QImage, QIcon
from PIL import Image, ImageEnhance
import pytesseract
import os
import subprocess

class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasText():
            self.insertPlainText(source.text())
        else:
            super().insertFromMimeData(source)

class NavisionFilter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The BETTER Navision")
        self.resize(600, 500)
        self.setMinimumSize(600, 500)
        self.setMaximumSize(700, 700)
        self.setWindowIcon(QIcon(self.resource_path("Pictures\\KTNlogo.ico")))

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Top buttons layout
        buttons_layout = QHBoxLayout()

        self.btn_filter_1 = QPushButton("Filter by |*")
        self.btn_filter_2 = QPushButton("Filter by |")
        self.btn_filter_3 = QPushButton("Filter by &&<>")
        self.btn_tesseract = QPushButton("Screenshot -> Text")
        self.btn_clear = QPushButton("Clear")

        buttons_layout.addWidget(self.btn_filter_1)
        buttons_layout.addWidget(self.btn_filter_2)
        buttons_layout.addWidget(self.btn_filter_3)
        buttons_layout.addWidget(self.btn_tesseract)
        buttons_layout.addWidget(self.btn_clear)

        # Text input area
        self.text_edit = PlainTextEdit()
        self.text_edit.setPlaceholderText("Paste your text here 📝")
        
        bg_path = self.resource_path("Pictures/KatoenNatie.png").replace("\\", "/")
        # CSS Styling
        self.text_edit.setStyleSheet(f"""
        QTextEdit{{
            background-image: url("{bg_path}");
            background-repeat: no-repeat;
            background-position: center;
            padding: 1px;
            font-size: 15px;
            font-family: Arial;
                                     }}
""")
        self.setStyleSheet("""
        QPushButton{
            font-size: 15px;
            font-family: Georgia;
            padding: 3px;
            border: 1px solid;
            border-radius: 5px;
            background-color: #e3e3e3;
            font-weight: bold;                       
                                     }
        QPushButton:hover{
            background-color: #a6aba7;               
                           }
        QPushButton:pressed{
            background-color: #ed1818;               
                           }              
""")

        # Add layouts/widgets
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.text_edit)

        # Connect buttons
        self.btn_filter_1.clicked.connect(self.apply_filter_1)
        self.btn_filter_2.clicked.connect(self.apply_filter_2)
        self.btn_filter_3.clicked.connect(self.apply_filter_3)
        self.btn_tesseract.clicked.connect(self.read_clipboard)
        self.btn_clear.clicked.connect(self.clear_text)

    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def apply_filter_1(self):
        text = self.text_edit.toPlainText()
        
        words = text.split()
        result = "|".join(f"*{w}" for w in words)

        self.text_edit.setPlainText(result)

    def apply_filter_2(self):
        text = self.text_edit.toPlainText()
        
        words = text.split()
        result = "|".join(words)

        self.text_edit.setPlainText(result)

    def apply_filter_3(self):
        text = self.text_edit.toPlainText()
        words = text.split()

        result = ""

        for w in range(len(words)):
            result += words[w]

            if w != len(words) - 1:
                result += "&<>"

        self.text_edit.setPlainText(result)

    def read_clipboard(self):
        installer_path = self.resource_path(
    os.path.join("OCR_tesseract_installer", "tesseract-ocr-w64-setup.exe")
        )

        if not self.ensure_tesseract():
            if os.path.exists(installer_path):
                QMessageBox.information(
                    self,
                    "Tesseract missing",
                    "Tesseract OCR is not installed.\nThe installer will now run."
                )
                os.startfile(installer_path)
                QMessageBox.information(
                    self,
                    "Restart required",
                    "Please restart the application after installation."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Tesseract installer not found!"
                )
            return
        
        clipboard = QApplication.clipboard()
        qimg = clipboard.image()

        if qimg.isNull():
            QMessageBox.warning(self, "Clipboard empty", "No image in clipboard!")
            return
        
        buffer = qimg.bits().asstring(qimg.byteCount())
        img = Image.frombytes(
            "RGBA",
            (qimg.width(), qimg.height()),
            buffer
        )

        # Accuracy processing
        img = img.convert("L")
        img = img.resize(
            (img.width * 2, img.height * 2),
            Image.LANCZOS
        )
        img = ImageEnhance.Contrast(img).enhance(1.8)
        img = img.point(lambda x: 255 if x > 200 else x)

        config = "--oem 3 --psm 6"
        text = pytesseract.image_to_string(
            img,
            lang="eng+nld",
            config=config
        )

        self.text_edit.setPlainText(text)
        print(f"installed here: {installer_path}")
    
    def clear_text(self):
        self.text_edit.clear()

    def ensure_tesseract(self):
        try:
            subprocess.run(
                ["tesseract", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except FileNotFoundError:
            pass

        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"H:\Tesseract\tesseract.exe",
            r"H:\Oleg\Tesseract+Navision\tesseract.exe"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NavisionFilter()
    window.show()
    sys.exit(app.exec_())

