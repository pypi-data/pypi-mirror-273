# PySideX
Unofficial PySide6 library, produced with the aim of facilitating the construction of more elegant and improved interfaces using PySide6 technology

# How to import
import *PySideX* as *px*

# Class
class App(px.*Window*):
    def __init__(
        self,
        title="PySideX 0.0.9",
        min_width=240,
        min_height=90,
        width=1280,
        height=720,
        icon="assets/ico/icon.ico",
    ):
        self._title = title
        self._min_width = min_width
        self._min_height = min_height
        self._width = width
        self._height = height
        self._icon = icon
        super().__init__(
            self._title,
            self._min_width,
            self._min_height,
            self._width,
            self._height,
            self._icon,
        )

# How to start
if __name__ == "__main__":
    app = px.*QApplication*(px.sys.argv)
    window = *App*()
    window.*show*()
    px.sys._exit_(app._exec_())
