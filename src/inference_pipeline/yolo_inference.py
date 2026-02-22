import asyncio
from ultralytics import YOLO
from src.inference_pipeline.base import InferenceBackend, InferenceOutput, Detection


class YoloBackend(InferenceBackend):
    def __init__(self, model_path: str, device: str = "cpu"):
        self.model = YOLO(model_path)
        self.model.to(device)

    def _parse(self, results, task: str) -> InferenceOutput:
        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for i, box in enumerate(r.boxes):
                polygon = None
                if task == "segment" and r.masks is not None:
                    polygon = r.masks.xy[i][0].tolist()
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                detections.append(Detection(
                    class_name=self.model.names[int(box.cls[0])],
                    confidence=float(box.conf[0]),
                    x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max,
                    polygon=polygon
                ))
        return InferenceOutput(detections=detections)

    async def predict(self, image_path: str) -> InferenceOutput:
        loop = asyncio.get_running_loop()
        results = await loop.run_in_executor(
            None, lambda: self.model.predict(image_path, task="detect")
        )
        return self._parse(results, "detect")

    async def segment(self, image_path: str) -> InferenceOutput:
        loop = asyncio.get_running_loop()
        results = await loop.run_in_executor(
            None, lambda: self.model.predict(image_path, task="segment")
        )
        return self._parse(results, "segment")
