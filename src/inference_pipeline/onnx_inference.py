import asyncio
import numpy as np
from src.inference_pipeline.base import InferenceBackend, InferenceOutput, Detection


class OnnxBackend(InferenceBackend):
    """
    ONNX Runtime backend. Plug in any ONNX-exported model.
    Expected model input: [1, 3, H, W] float32 normalized.
    Expected model output: [N, 6] → [x_min, y_min, x_max, y_max, confidence, class_id]
    """

    def __init__(self, model_path: str, class_names: list[str], input_size: tuple = (640, 640)):
        import onnxruntime as ort
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.class_names = class_names
        self.input_size = input_size
        self.input_name = self.session.get_inputs()[0].name

    def _preprocess(self, image_path: str) -> np.ndarray:
        import cv2
        img = cv2.imread(image_path)
        img = cv2.resize(img, self.input_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        return np.transpose(img, (2, 0, 1))[np.newaxis]  # [1, 3, H, W]

    def _run(self, image_path: str) -> list:
        tensor = self._preprocess(image_path)
        return self.session.run(None, {self.input_name: tensor})[0]

    def _parse(self, raw_output) -> InferenceOutput:
        detections = []
        for row in raw_output:
            x_min, y_min, x_max, y_max, conf, cls_id = row[:6]
            detections.append(Detection(
                class_name=self.class_names[int(cls_id)],
                confidence=float(conf),
                x_min=float(x_min), y_min=float(y_min),
                x_max=float(x_max), y_max=float(y_max),
            ))
        return InferenceOutput(detections=detections)

    async def predict(self, image_path: str) -> InferenceOutput:
        loop = asyncio.get_running_loop()
        raw = await loop.run_in_executor(None, lambda: self._run(image_path))
        return self._parse(raw)

    async def segment(self, image_path: str) -> InferenceOutput:
        # Segmentation requires a seg-head model; falls back to detect for now
        return await self.predict(image_path)
