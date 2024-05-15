from typing import Dict

import detectools.metrics.functionnals as F
from detectools.formats import BaseFormat
from detectools.metrics.base import (ClassifMetric, DetectMetric,
                                     SemanticSegmentationMetric)
from torch import Tensor
from torchmetrics.detection import MeanAveragePrecision


class DetectF1score(DetectMetric):
    """F1 score for detection task.

    Args:
        iou_threshold (``float``): IoU threshold to consider taht prediction and target boxes match. Default to 0.5.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.f1score, name="DetectF1score", *args, **kwargs)


class DetectPrecision(DetectMetric):
    """Precision for detection task.

    Args:
        iou_threshold (``float``): IoU threshold to consider taht prediction and target boxes match. Default to 0.5.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.precision, name="DetectPrecision", *args, **kwargs)


class DetectRecall(DetectMetric):
    """Recall for detection task.

    Args:
        iou_threshold (``float``): IoU threshold to consider taht prediction and target boxes match. Default to 0.5.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.recall, name="DetectRecall", *args, **kwargs)


class MeanAP(MeanAveragePrecision):
    """Compute Mean Average Precision (from torchmetrics MAP_ ).

    .. _MAP:
        https://lightning.ai/docs/torchmetrics/stable/detection/mean_average_precision.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.name = "MeanAP"

    def prepare_input(self, input: BaseFormat) -> Dict[str, Tensor]:
        """Transform BaseFormat into MAp inputs type.

        Args:
            input (``BaseFormat``): BaseFormat to convert.

        Returns:
            ``Dict[str, Tensor]``:
                - Dict of values for MAP computation.
        """
        boxes, labels = input.get(["boxes", "labels"])
        prepared = {"boxes": boxes, "labels": labels}
        if "scores" in input:
            prepared.update({"scores": input.get("scores")})
        return [prepared]

    def update(self, prediction: BaseFormat, target: BaseFormat):
        """Prepare inputs and call MAP.

        Args:
            prediction (``BaseFormat``): Predictions.
            target (``BaseFormat``): Targets.
        """
        prediction = self.prepare_input(prediction)
        target = self.prepare_input(target)
        super().update(prediction, target)


## classification metrics


class ClassifF1score(ClassifMetric):
    """F1 score for classification task.

    Args:
        num_classes (``int``): Number of classes for the task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(func=F.f1score, name="ClassifF1score", *args, **kwargs)

class ClassifPrecision(ClassifMetric):
    """F1 score for classification task.

    Args:
        num_classes (``int``): Number of classes for the task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(func=F.precision, name="ClassifPrecision", *args, **kwargs)

class ClassifRecall(ClassifMetric):
    """F1 score for classification task.

    Args:
        num_classes (``int``): Number of classes for the task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(func=F.recall, name="ClassifRecall", *args, **kwargs)


## semantic segmentation metrics


class SemanticF1score(SemanticSegmentationMetric):
    """F1 score for semantic segmentation task.

    Args:
        num_classes (``int``): Number of classes for the task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(func=F.f1score, name="SemanticF1score", *args, **kwargs)


class SemanticIoU(SemanticSegmentationMetric):
    """IoU for semantic segmentation task.

    Args:
        num_classes (``int``): Number of classes for the task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(func=F.iou, name="SemanticIoU", *args, **kwargs)


class SemanticAccuracy(SemanticSegmentationMetric):
    """Accuracy for semantic segmentation task.

    Args:
        num_classes (``int``): Number of classes for the task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(func=F.accuracy, name="SemanticAccuracy", *args, **kwargs)