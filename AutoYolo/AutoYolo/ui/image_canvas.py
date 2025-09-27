"""Graphics view used to render images and annotations."""
from __future__ import annotations

from typing import List

from PySide6 import QtCore, QtGui, QtWidgets

from ..core.project import Annotation


class ImageCanvas(QtWidgets.QGraphicsView):
    box_color = QtGui.QColor(255, 99, 71)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setDragMode(self.ScrollHandDrag)
        self._scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self._scene)
        self._pixmap_item: QtWidgets.QGraphicsPixmapItem | None = None
        self._box_items: List[QtWidgets.QGraphicsItem] = []
        self._current_pixmap: QtGui.QPixmap | None = None

    def set_image(self, pixmap: QtGui.QPixmap) -> None:
        self._scene.clear()
        self._box_items.clear()
        self._pixmap_item = self._scene.addPixmap(pixmap)
        self._current_pixmap = pixmap
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        if self._pixmap_item is not None:
            self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def set_boxes(self, annotations: List[Annotation], image_size: tuple[int, int]) -> None:
        if self._pixmap_item is None:
            return
        for item in self._box_items:
            self._scene.removeItem(item)
        self._box_items.clear()
        width, height = image_size
        for ann in annotations:
            rect = self._annotation_to_rect(ann, width, height)
            pen = QtGui.QPen(self.box_color)
            pen.setWidthF(2.0)
            box_item = self._scene.addRect(rect, pen)
            self._box_items.append(box_item)
            label_item = self._scene.addSimpleText(ann.label)
            label_item.setBrush(QtGui.QBrush(self.box_color))
            label_item.setPos(rect.topLeft())
            self._box_items.append(label_item)

    def _annotation_to_rect(self, ann: Annotation, width: int, height: int) -> QtCore.QRectF:
        x_center = ann.x_center * width
        y_center = ann.y_center * height
        box_w = ann.width * width
        box_h = ann.height * height
        top_left = QtCore.QPointF(x_center - box_w / 2, y_center - box_h / 2)
        return QtCore.QRectF(top_left, QtCore.QSizeF(box_w, box_h))
