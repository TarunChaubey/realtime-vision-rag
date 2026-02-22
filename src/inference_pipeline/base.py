from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Detection:
    class_name: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    polygon: Optional[List[float]] = None


@dataclass
class InferenceOutput:
    detections: List[Detection] = field(default_factory=list)


class InferenceBackend(ABC):
    """All backends must implement this interface."""

    @abstractmethod
    async def predict(self, image_path: str) -> InferenceOutput:
        """Run object detection."""

    @abstractmethod
    async def segment(self, image_path: str) -> InferenceOutput:
        """Run instance segmentation."""
