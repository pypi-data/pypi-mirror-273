from abc import abstractclassmethod
from typing import Any, Dict, Literal, Tuple, Union

from detectools.formats import BaseFormat, BatchedFormats
from torch import Tensor
from torch.nn import Module


class BaseModel(Module):
    """Base Class for detectools models.

    Attributes:
    -----------

    Attributes:
        confidence_thr (``float``): Confidence score threshold to consider object as true prediction.
        max_detection (``int``): Maximum number of object to predict on one image.
        nms_threshold (``float``): IoU threshold to consider 2 boxes as overlapping for Non Max Suppression algorithm.
        num_classes (``int``): Number of classes. 
    
    Methods:
    -----------
    """

    confidence_thr: float = 0.5
    max_detection: int = 300
    nms_threshold: float = 0.45
    num_classes: int = 1

    @classmethod
    def to_device(self, device: Literal["cpu", "cuda"]):
        """Send model to device.

        Args:
            device (``Literal['cpu', 'cuda']``): Device to send model on.
        """

    @classmethod
    def prepare(
        self, images: Tensor, targets: BatchedFormats = None
    ) -> Union[Any, Tuple[Any]]:
        """Transform images and targets into model specific format for prediction & loss computation.

        Args:
            images (``Tensor``): Batch images.
            targets (``BatchedFormats``, **optional**): Batched targets from DetectionDataset.

        Returns:
            ``Union[Any, Tuple[Any]]``:
                - Images data prepared for model.
                - If targets: images + targets prepared for model.
        """
        

    @classmethod
    def build_results(self, raw_outputs: Any) -> BatchedFormats:
        """Transform model outputs into BaseFormat for results.
        This function also apply instances selection on results according to args:

        - confidence_thr
        - max_detection
        - nms_threshold

        Args:
            raw_outputs (``Any``): Model outputs.

        Returns:
            ``BatchedFormats``:
                - Model output for batch.
        """

    @classmethod
    def get_predictions(self, images: Tensor) -> BatchedFormats:
        """Prepare images, Apply model forward pass and build results.

        Args:
            images (``Tensor``): RGB images Tensor.

        Returns:
            ``BatchedFormats``:
                - Predictions for images as BatchedFormats.
        """

    @classmethod
    def run_forward(
        self, images: Tensor, targets: BatchedFormats, predict: bool = False
    ) -> Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormats]]:
        """Compute loss from images and if target passed, compute loss & return both loss dict
        and results.

        Args:
            images (``Tensor``): Batch RGB images.
            targets (``BatchedFormats``): Batch targets.
            predict (``bool``, **optional**): To return predictions or not. Defaults to False.

        Returns:
            ``Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormats]]``:
                - Loss dict.
                - If predict: Predictions.
        """
