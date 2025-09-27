"""Detection backend abstraction."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

from ..core.device import resolve_device


@dataclass(slots=True)
class DetectionResult:
    boxes: np.ndarray
    scores: np.ndarray
    labels: List[str]
    size: tuple[int, int]


class AutoDetector:
    def __init__(self, weights: str | Path, *, preferred_device: str | None = None) -> None:
        self.weights = str(weights)
        self.device = resolve_device(preferred_device)
        self._model = None

    def _ensure_model(self) -> None:
        if self._model is not None:
            return
        from ultralytics import YOLO

        self._model = YOLO(self.weights)
        if self.device.type == "dml":
            try:
                self._model.to("dml")
            except Exception:  # fallback to cpu if directml unavailable
                self._model.to("cpu")
        else:
            self._model.to(self.device.torch_device)

    def run(self, image_path: Path, conf: float, classes: List[str] | None = None) -> DetectionResult:
        self._ensure_model()
        results = self._model.predict(
            source=str(image_path),
            conf=conf,
            verbose=False,
            device=self.device.torch_device,
            classes=classes,
        )
        prediction = results[0]
        boxes = prediction.boxes.xyxy.cpu().numpy()
        scores = prediction.boxes.conf.cpu().numpy()
        ids = prediction.boxes.cls.cpu().numpy().astype(int)
        labels = [prediction.names[i] for i in ids]
        size = (int(prediction.orig_shape[1]), int(prediction.orig_shape[0]))
        return DetectionResult(boxes=boxes, scores=scores, labels=labels, size=size)
