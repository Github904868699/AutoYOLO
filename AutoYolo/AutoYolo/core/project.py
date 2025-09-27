"""Dataset and annotation helpers."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List

import json

YOLO_SUFFIX = ".txt"


@dataclass(slots=True)
class Annotation:
    label: str
    x_center: float
    y_center: float
    width: float
    height: float


@dataclass
class ImageEntry:
    path: Path
    annotations: List[Annotation] = field(default_factory=list)

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def annotation_path(self) -> Path:
        return self.path.with_suffix(YOLO_SUFFIX)


class AnnotationProject:
    def __init__(self, root: Path):
        self.root = root
        if not root.exists():
            raise FileNotFoundError(f"未找到数据集目录: {root}")
        self.images: List[ImageEntry] = []
        self._load()

    def _load(self) -> None:
        image_paths = sorted(
            [p for p in self.root.rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]
        )
        self.images = [ImageEntry(p) for p in image_paths]
        for entry in self.images:
            entry.annotations = self._read_annotation(entry.annotation_path)

    def _read_annotation(self, path: Path) -> List[Annotation]:
        if not path.exists():
            json_path = path.with_suffix(".json")
            if json_path.exists():
                data = json.loads(json_path.read_text("utf-8"))
                return [Annotation(**item) for item in data.get("annotations", [])]
            return []

        annotations: List[Annotation] = []
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                label, *coords = parts
                x_c, y_c, w, h = map(float, coords)
                annotations.append(Annotation(label, x_c, y_c, w, h))
        return annotations

    def save_annotation(self, entry: ImageEntry) -> None:
        path = entry.annotation_path
        if not entry.annotations:
            if path.exists():
                path.unlink()
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            for ann in entry.annotations:
                file.write(f"{ann.label} {ann.x_center:.6f} {ann.y_center:.6f} {ann.width:.6f} {ann.height:.6f}\n")

    def iter_images(self) -> Iterable[ImageEntry]:
        yield from self.images
