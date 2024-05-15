from __future__ import annotations

from typing import Any, Dict, List, Literal, Tuple, Union

import torch
from detectools import Task
from detectools.formats.base import BaseAnnotation, BaseFormat
from torch import Tensor
from torchvision.transforms.v2.functional import crop_bounding_boxes, pad_bounding_boxes
from torchvision.tv_tensors import BoundingBoxes


class DetectionAnnotation(BaseAnnotation):
    """BaseAnnotation child class for detection task.

    Attributes:
    -----------

    Attributes:
        boxe (``BoundingBoxes``): Boxe coordinates in XYWH format.
        label (``Tensor``): Class label of object.
        spatial_size (``Tuple[int, int]``): Size of corresponding image (H, W)
        score (``Tensor``): Confidence score of the object (for prediction). 
    
    Methods:
    -----------
    """

    boxe : BoundingBoxes
    label : Tensor
    spatial_size: Tuple[int, int]
    score: Tensor

    def __init__(
        self,
        spatial_size: Tuple[int],
        label: Tensor,
        boxe: Tensor,
        score: Tensor = None,
    ):

        self.boxe = boxe
        self.label = label
        self.spatial_size = spatial_size
        self.score = score

    def object_to_coco(
        self, annotation_id: int = 1, image_id: int = 1
    ) -> Dict[str, Any]:
        """Return detection annotation data as COCO like dict.

        Args:
            annotation_id (``int``, **optional**): Id of the annotation. Defaults to 1.
            image_id (``int``, **optional**): Id of the corresponding image. Defaults to 1.

        Returns:
            ``Dict[str, Any]``:
                - COCO like dict with Annotation instance data.
        """
        annotation = {
            "id": annotation_id,
            "bbox": self.boxe.tolist(),
            "category_id": self.label.item(),
            "image_id": image_id,
        }
        if isinstance(self.score, Tensor):
            annotation["score"] = self.score.item()

        return annotation


class DetectionFormat(BaseFormat):
    """BaseFormat child class for detection task.

    Args:
        spatial_size (``Tensor``): Spatial size (H, W) of corresponding images.
        labels (``Tensor``): Tensor of shape (N,) with class labels for each object.
        boxes (``Tensor``): Tensor of shape (N, 4). N for N objects and 4 for boxes coordinates.
        scores (``Tensor``, **optional**): Tensor of shape (N,) with objects confidence score. Defaults to None.
        box_format (``Literal['XYWH', 'XYXY', 'CXCYWH']``, **optional**): Format of bounding boxes. Defaults to 'XYWH'.
        
    
    Attributes:
    -----------

    Attributes:
        box_format (``Literal["XYWH", "XYXY", "CXCYWH"]``): Format of bounding boxes.
        spatial_size (``Tuple[int, int]``): Size of corresponding image (H, W)
        size (``int``): Number of objects in BaseFormat.
        data: (``Dict[str, Tensor]``): Data dict that contains objects informations in it's keys (labels, boxes, scores).
    
    Methods:
    -----------
    
    """
    spatial_size: Tuple[
        int, int
    ]  # Store the H, W image size corresponding to objects boxes/masks stored in BaseFormat.
    data: Dict[
        str, Tensor
    ]  # Store all values (labels, boxes/masks at least) corresponding to objects in an image.
    size: int  # Number of objects in image.
    box_format: Literal["XYWH", "XYXY", "CXCYWH"]  # format for bounding boxes.

    # override
    def empty(spatial_size: Tuple[int]) -> DetectionFormat:
        """Return an empty instance DetectionFormat.

        Args:
            spatial_size (``Tuple[int]``): Size (H, W) of the corresponding image.

        Returns:
            ``DetectionFormat``:
                - DetectionFormat instance.
        """
        boxes = BoundingBoxes([[]], canvas_size=spatial_size, format="XYWH")
        labels = torch.tensor([])
        detection_format = DetectionFormat(
            spatial_size=spatial_size,
            labels=labels,
            boxes=boxes,
        )
        return detection_format

    # override
    def from_coco(
        coco_annotations: List[Dict[str, Any]], spatial_size: Tuple[int]
    ) -> DetectionFormat:
        """Return DetectionFormat from an image COCO data dictionnary.

        Args:
            coco_annotations (``List[Dict[str, Any]]``): Coco data dictionnary.
            spatial_size (``Tuple[int]``): Size (H, W) of the corresponding image.

        Returns:
            ``DetectionFormat``:
                - DetectionFormat instance.
        """
        boxes = torch.tensor([ann["bbox"] for ann in coco_annotations])
        labels = torch.tensor([ann["category_id"] for ann in coco_annotations])
        detection_format = DetectionFormat(spatial_size, labels, boxes)
        return detection_format

    def __init__(
        self,
        spatial_size: Tensor,
        labels: Tensor,
        boxes: Tensor,
        scores: Tensor = None,
        box_format: Literal["XYWH", "XYXY", "CXCYWH"] = "XYWH",
    ):
        
        # assert Task mode is "instance_segmentation"
        assert (
            Task.mode == "detection"
        ), f"Task mode should be 'detection' to construct DetectionFormat object, got {Task.mode}."

        self.spatial_size = spatial_size
        self.size = labels.nelement()
        self.box_format = box_format
        # send to tv_tensor
        boxes: Tensor = BoundingBoxes(
            boxes.int(), canvas_size=spatial_size, format=box_format
        )
        # store all data in data dict
        self.data: Dict[str, Tensor] = {"boxes": boxes, "labels": labels}
        if scores != None:
            self.data["scores"] = scores

    def __getitem__(self, indexes: Union[int, Tensor]) -> DetectionFormat:
        """ Return a subset DetectionFormat by keeping only elements of data dict values (tensors) at positions of indexes.

        Args:
            indexes (``Union[int, Sequence[int]]``): Indexes to slice objects data.

        Returns:
            ``DetectionFormat``:
                - DetectionFormat with n objects for n indexes in indexes.
        """
        sliced = super().__getitem__(indexes)
        if "boxes" in self:
            boxes = self.get("boxes")[indexes]
            boxes = BoundingBoxes(
                boxes,
                canvas_size=self.spatial_size,
                format=self.box_format,
                device=self.get_device(),
            )
            sliced.data["boxes"] = boxes

        return sliced

    def get_object(self, indice: int) -> DetectionAnnotation:
        """Return DetectionAnnotation object at position indice.

        Args:
            indice (``int``): Position of object to gather.

        Returns:
            ``DetectionAnnotation``:
                - DetectionAnnotation instance.
        """
        single_object_format = self[indice]
        bbox, label = single_object_format.get("boxes", "labels")
        detection_object = DetectionAnnotation(self.spatial_size, label, bbox.squeeze())
        if "scores" in single_object_format:
            detection_object.score = single_object_format.get("scores")

        return detection_object

    # Methods that changes internal states of Formats
    # override
    def crop(self, top: int, left: int, height: int, width: int):
        """Crop boxes from top corner pixel and update spatial size.

        Args:
            top (``int``): Position to crop from top border.
            left (``int``): Position to crop from left border.
            height (``int``): height of the crop.
            width (``int``): Width of the crop.
        """
        if self.size == 0:
            self.spatial_size = (height, width)
            return self
        boxes = self.get("boxes")
        boxes, canvas_size = crop_bounding_boxes(
            boxes,
            format=self.box_format,
            top=top,
            left=left,
            height=height,
            width=width,
        )
        self.set(
            "boxes",
            BoundingBoxes(
                boxes,
                canvas_size=canvas_size,
                format=self.box_format,
                device=self.get_device(),
            ),
        )
        self.spatial_size = canvas_size

    # override
    def pad(self, left: int, top: int, right: int, bottom: int):
        """Pad boxes and update spatial size.

        Args:
            left (``int``): Pad value on left border.
            top (``int``): Pad value on top border.
            right (``int``): Pad value on right border.
            bottom (``int``): Pad value on bottom border.
        """
        if self.size == 0:
            h, w = self.spatial_size
            self.spatial_size = (h + top + bottom, w + left + right)
            return

        boxes: BoundingBoxes = self.get("boxes")
        boxes, canvas_size = pad_bounding_boxes(
            boxes,
            self.box_format,
            self.spatial_size,
            list((left, top, right, bottom)),
        )
        self.set(
            "boxes",
            BoundingBoxes(
                boxes,
                canvas_size=canvas_size,
                format=self.box_format,
                device=self.get_device(),
            ),
        )
        self.spatial_size = canvas_size
