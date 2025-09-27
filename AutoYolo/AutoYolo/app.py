"""Application entry point."""
from __future__ import annotations

import os
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from .ui.main_window import MainWindow

QSS_PATH = Path(__file__).resolve().parent / "assets" / "qss" / "dark.qss"


def load_stylesheet(app: QtWidgets.QApplication) -> None:
    try:
        import qdarktheme

        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    except Exception:
        if not QSS_PATH.exists():
            return
        with QSS_PATH.open("r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def run() -> None:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setOrganizationName("AutoYolo")
    app = QtWidgets.QApplication()
    app.setWindowIcon(QtGui.QIcon())
    load_stylesheet(app)
    window = MainWindow()
    default_dataset = os.environ.get("AUTOYOLO_DATASET")
    if default_dataset:
        try:
            window.load_project(Path(default_dataset))
        except Exception as exc:  # pragma: no cover - best effort auto load
            print(f"无法加载预设数据集: {exc}")
    window.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover
    run()
