from math import ceil, floor
from typing import Any, Dict, List, Literal, Tuple, Union

import torch
import torchvision.transforms.v2.functional as F
from detectools import Task
from detectools.formats import BatchedFormats, DetectionFormat
from detectools.models.base import BaseModel
from torch import Tensor
from ultralytics.cfg import get_cfg
from ultralytics.models.yolo.detect.train import DetectionModel
from ultralytics.nn.tasks import attempt_load_one_weight
from ultralytics.utils import DEFAULT_CFG


class YoloDetection(DetectionModel, BaseModel):
    """YOLO detection model class in detectools. This class inheriths from DetectionModel_ (Ultralytics) and BaseModel (detectools).
    Load yolo architecture from ultralytics repository. If pretrained load a pretrain model from ultralytics.

    .. _DetectionModel:
            https://docs.ultralytics.com/reference/nn/tasks/?h=detectionmodel#ultralytics.nn.tasks.DetectionModel.__init__

    Args:
        architecture (``str``, **optional**): Architecture to use to build YOLO model. Check Ultralytics availables architectures_ . Defaults to "yolov8m".
        num_classes (``int``, **optional**): Number of classes in the task. Defaults to 1.
        pretrained (``bool``, **optional**): To use pretrained weights. Defaults to True.
        confidence_thr (``float``, **optional**): Confidence score threshold to consider object as true prediction. Defaults to 0.5.
        max_detection (``int``, **optional**): Maximum number of object to predict on one image. Defaults to 300.
        nms_threshold (``float``, **optional**): IoU threshold to consider 2 boxes as overlapping for Non Max Suppression algorithm.. Defaults to 0.45.
    
    .. _architectures:
        https://docs.ultralytics.com/models/yolov8/#supported-tasks-and-modes

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

    def __init__(
        self,
        architecture: str = "yolov8m",
        num_classes: int = 1,
        pretrained=True,
        confidence_thr: float = 0.5,
        max_detection: int = 300,
        nms_threshold: float = 0.45,
        *args,
        **kwargs,
    ):
        
        # assert Task mode is "instance_segmentation"
        assert (
            Task.mode == "detection"
        ), f"Task mode should be 'detection' to construct YoloDetection object, got {Task.mode}"
        # build model from ultralytics config
        super().__init__(f"{architecture}.yaml", nc=num_classes, *args, **kwargs)
        self.args = get_cfg(DEFAULT_CFG)
        self.criterion = self.init_criterion()
        self.confidence_thr = confidence_thr
        self.max_detection = max_detection
        self.nms_threshold = nms_threshold
        self.num_classes = num_classes
        # load weights from ultralytics repo if pretrained
        if pretrained:
            architecture = attempt_load_one_weight(
                f"{architecture}.pt",
            )
            self.load(architecture[0])

    # override
    def to_device(self, device: Literal["cpu", "cuda"]):
        """Send model & criterion to device.

        Args:
            device (``Literal['cpu', 'cuda']``): Device to send model on.
        """
        self.to(device)
        self.criterion = self.init_criterion()

    def prepare_image(self, images: Tensor) -> Tuple[Tensor, Tuple[int]]:
        """Pad images if needed & return padding values.

        Args:
            images (``Tensor``): Batch_images.

        Returns:
            ``Tuple[Tensor, Tuple[int]]``:
                - Padded images.
                - Padding values.
        """
        # get borders padding
        padding_values = self.yolo_pad_requirements(images)
        # pad images
        images = F.pad(images, list(padding_values))
        return images, padding_values

    def prepare_target(self, targets: BatchedFormats) -> Dict[str, Tensor]:
        """Transform DetectionFormat targets into yolo targets format.

        Args:
            targets (``BatchedFormats``): Batch targets.

        Returns:
            ``Dict[str, Tensor]``:
                - Targets in YOLO format.
        """
        # transform boxes
        targets.apply("set_boxes_format", "CXCYWH")
        targets.apply("normalize")
        # get values
        targets: List[DetectionFormat] = targets.split()
        boxes = torch.cat([t.get("boxes") for t in targets])
        labels = torch.cat([t.get("labels") for t in targets])
        device = labels.device
        images_indices = torch.cat(
            [torch.full((t.size,), i, device=device) for i, t in enumerate(targets)]
        )
        # reshape data to fit YoloV8detection loss
        indexes = images_indices[..., None]
        classes = labels[..., None]

        batch_targets = {"batch_idx": indexes, "cls": classes, "bboxes": boxes}

        return batch_targets

    # override
    def prepare(
        self, images: Tensor, targets: BatchedFormats = None
    ) -> Union[Tensor, Tuple[Tensor, Dict[str, Tensor]]]:
        """Transform images and targets into YOLO specific format for prediction & loss computation.

        Args:
            images (``Tensor``): Batch images.
            targets (``BatchedFormats``, **optional**): Batched targets from DetectionDataset.

        Returns:
            ``Union[Tensor, Tuple[Tensor, Dict[str, Tensor]]]``:
                - Images data prepared for YOLO.
                - If targets: images + targets prepared for YOLO.
        """

        (left, top, right, bottom) = self.yolo_pad_requirements(images)
        # pad images & target
        images = F.pad(images, list((left, top, right, bottom)))
        if targets:
            prepared_targets = targets.clone()
            # prepare targets for yolo
            prepared_targets.apply("pad", left, top, right, bottom)
            prepared_targets = self.prepare_target(prepared_targets)
            return images, prepared_targets
        else:
            return images

    def yolo_pad_requirements(
        self, input_object: Union[Tensor, DetectionFormat]
    ) -> List[int]:
        """Return values for padding to fit 'divisible by 32' requirement.

        Args:
            input_object (``Union[Tensor, DetectionFormat]``): Input to pad (image or DetectionFormat).

        Returns:
            ``List[int]``:
                - Padding values.
        """
        # get spatial size
        if isinstance(input_object, DetectionFormat):
            h, w = input_object.spatial_size
        elif isinstance(input_object, Tensor):
            h, w = input_object.shape[-2:]  # (H,W)
        # get pad values
        diff_h, diff_w = h % 32, w % 32
        pad_h = 32 - diff_h if diff_h > 0 else 0
        pad_w = 32 - diff_w if diff_w > 0 else 0
        # define padding for each border
        if pad_h or pad_w:
            half_h, half_w = pad_h / 2, pad_w / 2
            left, top, right, bottom = (
                ceil(half_w),
                ceil(half_h),
                floor(half_w),
                floor(half_h),
            )
        else:
            left, top, right, bottom = (0, 0, 0, 0)
        return (left, top, right, bottom)

    def retrieve_spatial_size(self, raw_outputs: List[Tensor]) -> Tuple[int]:
        """Retrieve image shape from raw_outputs and stride values.

        Args:
            raw_outputs (``List[Tensor]``): Raw ouptuts from YOLO model.

        Returns:
            ``Tuple[int]``:
                - Size of input image (H, W).
        """
        h = int(raw_outputs[0].shape[-2] * self.stride[0])
        w = int(raw_outputs[0].shape[-1] * self.stride[0])
        return (h, w)

    # override
    def build_results(
        self, raw_outputs: List[Tensor], prebuild_outputs: Tensor
    ) -> BatchedFormats:
        """Transform model outputs into Batch DetectionFormat for results.

        Args:
            raw_outputs (``List[Tensor]``): Model outputs.
            prebuild_outputs (``Tensor``): Extracted boxes from YOLO raw outputs.

        Returns:
            ``BatchedFormats``:
                - Batched predictions.
        """

        prebuild_outputs = prebuild_outputs.unbind()
        h, w = self.retrieve_spatial_size(raw_outputs)
        # create empty Format to merge batch results
        results = []
        # for each prediction
        for prediction in prebuild_outputs:
            # send pred in good pshape
            prediction = prediction.permute(1, 0)
            # get best class and corresponding score
            best_class = torch.argmax(prediction[:, 4:], dim=1)
            confidence = torch.max(prediction[:, 4:], dim=1)
            # gather box cxcywh coordinates
            boxes_coordinates = prediction[:, :4]
            # build result
            result = DetectionFormat(
                spatial_size=(h, w),
                boxes=boxes_coordinates,
                labels=best_class,
                scores=confidence.values,
                box_format="CXCYWH",
            )
            # convert boxes in coco
            result.set_boxes_format("XYWH")
            # objects selections
            result = result.confidence(self.confidence_thr)
            result = result.nms(self.nms_threshold)
            result = result.max_detections(self.max_detection)
            # stack batch results
            results.append(result)

        if len(results) == 0:
            results = DetectionFormat.empty((h, w))

        results = BatchedFormats(results)
        return results

    def compute_loss(
        self, raw_outputs: Tensor, targets: Dict[str, Tensor]
    ) -> Dict[str, Tensor]:
        """Compute loss with predictions & targets.

        Args:
            raw_outputs (``Any``): Raw output of model.
            targets (``DetectionFormat``): Targets in YOLO format.

        Returns:
            ``Dict[str, Tensor]``:
                - Loss dict with total loss (key: "loss") & sublosses.
        """
        loss, loss_detail = self.criterion(raw_outputs, targets)
        loss_dict = {
            "loss": loss,
            "loss_box": loss_detail[0],
            "loss_cls": loss_detail[1],
            "loss_dfl": loss_detail[2],
        }
        return loss_dict

    # override
    def run_forward(
        self,
        images: Tensor,
        targets: BatchedFormats,
        predict: bool = False,
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
                - If predict: predictions.
        """
        assert predict == (
            not self.training
        ), f"Model mode should be equal to predict boolean, got {self.training} & {predict}"
        # prepare inputs
        prepared_images, prepared_targets = self.prepare(images, targets=targets)
        # run forward pass
        if self.training:
            raw_outputs = self(prepared_images)
        else:
            prebuild_output, raw_outputs = self(prepared_images)
        # compute loss
        loss_dict = self.compute_loss(raw_outputs, prepared_targets)
        # return predictions if needed
        if predict:
            predictions = self.build_results(raw_outputs, prebuild_output)
            left, top, _, _ = self.yolo_pad_requirements(images)
            h, w = images.shape[-2:]
            predictions.apply("crop", top, left, h, w)
            return loss_dict, predictions
        else:
            return loss_dict

    # override
    def get_predictions(self, images: Tensor) -> BatchedFormats:
        """Prepare images, Apply YOLO forward pass and build results.

        Args:
            images (``Tensor``): RGB images Tensor.

        Returns:
            ``BatchedFormats``:
                - Predictions for images as BatchedFormats.
        """
        self.eval()
        # get original spatial size
        ori_h, ori_w = images.shape[-2:]
        # pad images
        images, (left, top, _, _) = self.prepare_image(images)
        # predict
        prebuild_output, raw_outputs = self(images)
        results = self.build_results(raw_outputs, prebuild_output)
        # crop to back at original spatial size
        results.apply("crop", top, left, ori_h, ori_w)

        return results
