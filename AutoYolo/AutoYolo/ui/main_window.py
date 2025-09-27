"""Main window for the AutoYolo studio."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from ..core.annotator import AutoLabelConfig, AutoLabeler
from ..core.project import AnnotationProject, ImageEntry
from .image_canvas import ImageCanvas


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AutoYolo 标注工作室")
        self.resize(1280, 720)
        self._project: Optional[AnnotationProject] = None
        self._current_index: int = -1
        self._auto_labeler: Optional[AutoLabeler] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._canvas = ImageCanvas()
        self._info_panel = self._create_info_panel()

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self._canvas)
        splitter.addWidget(self._info_panel)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        toolbar = QtWidgets.QToolBar("主工具栏")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QtGui.QAction("打开数据集", self)
        open_action.triggered.connect(self.open_folder_dialog)
        toolbar.addAction(open_action)

        auto_label_action = QtGui.QAction("自动标注当前", self)
        auto_label_action.triggered.connect(self.auto_label_current)
        toolbar.addAction(auto_label_action)

        auto_all_action = QtGui.QAction("批量标注全部", self)
        auto_all_action.triggered.connect(self.auto_label_all)
        toolbar.addAction(auto_all_action)

        next_action = QtGui.QAction("下一张", self)
        next_action.triggered.connect(self.show_next)
        toolbar.addAction(next_action)

        prev_action = QtGui.QAction("上一张", self)
        prev_action.triggered.connect(self.show_previous)
        toolbar.addAction(prev_action)

    def _create_info_panel(self) -> QtWidgets.QWidget:
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self._dataset_label = QtWidgets.QLabel("未加载数据集")
        self._dataset_label.setObjectName("datasetLabel")
        layout.addWidget(self._dataset_label)

        self._filename_label = QtWidgets.QLabel("文件名：-")
        layout.addWidget(self._filename_label)

        self._index_label = QtWidgets.QLabel("进度：0 / 0")
        layout.addWidget(self._index_label)

        self._device_label = QtWidgets.QLabel("推理设备：检测中…")
        layout.addWidget(self._device_label)

        layout.addSpacing(12)

        config_group = QtWidgets.QGroupBox("自动标注参数")
        form = QtWidgets.QFormLayout(config_group)
        self._confidence_spin = QtWidgets.QDoubleSpinBox()
        self._confidence_spin.setRange(0.05, 0.99)
        self._confidence_spin.setSingleStep(0.05)
        self._confidence_spin.setValue(0.25)
        form.addRow("置信度阈值", self._confidence_spin)
        layout.addWidget(config_group)

        layout.addStretch(1)
        self._status_label = QtWidgets.QLabel("状态：等待加载")
        self._status_label.setWordWrap(True)
        layout.addWidget(self._status_label)
        return panel

    # ------------------------------------------------------------------
    # Dataset management
    # ------------------------------------------------------------------
    def open_folder_dialog(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择图片文件夹")
        if directory:
            self.load_project(Path(directory))

    def load_project(self, root: Path) -> None:
        project = AnnotationProject(root)
        self._project = project
        self._dataset_label.setText(f"数据集：{root}")
        self._status_label.setText("状态：数据集已加载")
        self._auto_labeler = AutoLabeler(weights="yolov8n.pt", project=project)
        self._device_label.setText(f"推理设备：{self._auto_labeler.detector.device.description}")
        if not project.images:
            self._current_index = -1
            self._status_label.setText("状态：文件夹中没有可用图片")
            self._canvas.scene().clear()
            return
        self._current_index = 0
        self.show_current()

    def _current_entry(self) -> Optional[ImageEntry]:
        if not self._project or self._current_index < 0 or self._current_index >= len(self._project.images):
            return None
        return self._project.images[self._current_index]

    def show_current(self) -> None:
        entry = self._current_entry()
        if not entry:
            self._status_label.setText("状态：没有可展示的图片")
            return
        pixmap = QtGui.QPixmap(str(entry.path))
        if pixmap.isNull():
            self._status_label.setText("状态：无法加载图片")
            return
        self._canvas.set_image(pixmap)
        image_size = (pixmap.width(), pixmap.height())
        self._canvas.set_boxes(entry.annotations, image_size)
        self._filename_label.setText(f"文件名：{entry.path.name}")
        total = len(self._project.images) if self._project else 0
        self._index_label.setText(f"进度：{self._current_index + 1} / {total}")

    def show_next(self) -> None:
        if not self._project:
            return
        self._current_index = min(self._current_index + 1, len(self._project.images) - 1)
        self.show_current()

    def show_previous(self) -> None:
        if not self._project:
            return
        self._current_index = max(self._current_index - 1, 0)
        self.show_current()

    # ------------------------------------------------------------------
    # Auto labeling
    # ------------------------------------------------------------------
    def auto_label_current(self) -> None:
        entry = self._current_entry()
        if not entry or not self._auto_labeler:
            return
        conf = self._confidence_spin.value()
        self._status_label.setText("状态：正在自动标注当前图片…")
        QtWidgets.QApplication.processEvents()
        self._auto_labeler.auto_label([entry], AutoLabelConfig(score_threshold=conf))
        self._status_label.setText("状态：自动标注完成")
        self.show_current()

    def auto_label_all(self) -> None:
        if not self._project or not self._auto_labeler:
            return
        conf = self._confidence_spin.value()
        self._status_label.setText("状态：正在自动标注全部图片…")
        QtWidgets.QApplication.processEvents()
        self._auto_labeler.auto_label(self._project.iter_images(), AutoLabelConfig(score_threshold=conf))
        self._status_label.setText("状态：全部标注完成")
        self.show_current()
