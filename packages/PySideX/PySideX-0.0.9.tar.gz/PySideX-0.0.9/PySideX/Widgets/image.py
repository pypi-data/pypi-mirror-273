from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap


class Image(QLabel):
    def __init__(self,img,id="image") -> None:
        super().__init__()
        self._img = img
        self._id = id
        self.__config__()

    def __config__(self):
        self.setObjectName(self._id)
        self.setText('')
        self._setImageIcon()

    def _setImageIcon(self):
        if isinstance(self._img, str):
            pixmap = QPixmap(self._img)
            self.setPixmap(pixmap)
            self.setScaledContents(True)
        elif isinstance(self._img, bytes):
            pixmap = QPixmap()
            pixmap.loadFromData(self._img)
            self.setPixmap(pixmap)
            self.setScaledContents(True)
        else:
            raise ValueError("Unknown icon type")

    def click(self, target):
        """Every function expects to receive an event"""
        self.mousePressEvent = target

    def setStyleSheetFile(self, file):
        with open(file, "r") as f:
            css = f.read()
            self.setStyleSheet(css)

