"""Annotation orchestration layer."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from .project import Annotation, ImageEntry, AnnotationProject
from ..models.detector import AutoDetector, DetectionResult


@dataclass
class AutoLabelConfig:
    score_threshold: float = 0.25
    classes: Sequence[str] | None = None


class AutoLabeler:
    def __init__(self, weights: str | Path, project: AnnotationProject, *, device: str | None = None) -> None:
        self.project = project
        self.detector = AutoDetector(weights=weights, preferred_device=device)

    def auto_label(self, entries: Iterable[ImageEntry], config: AutoLabelConfig | None = None) -> None:
        config = config or AutoLabelConfig()
        for entry in entries:
            result = self.detector.run(entry.path, config.score_threshold, list(config.classes) if config.classes else None)
            entry.annotations = self._to_annotations(result, entry.path)
            self.project.save_annotation(entry)

    def _to_annotations(self, result: DetectionResult, path: Path) -> List[Annotation]:
        if result.boxes is None or len(result.boxes) == 0:
            return []
        width, height = result.size
        boxes = result.boxes
        labels = result.labels
        annotations: List[Annotation] = []
        for box, label in zip(boxes, labels):
            x1, y1, x2, y2 = box
            x_center = ((x1 + x2) / 2) / width
            y_center = ((y1 + y2) / 2) / height
            w = (x2 - x1) / width
            h = (y2 - y1) / height
            annotations.append(Annotation(label, x_center, y_center, w, h))
        return annotations
