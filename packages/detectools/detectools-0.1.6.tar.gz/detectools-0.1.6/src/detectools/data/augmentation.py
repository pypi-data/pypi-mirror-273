from typing import List, Tuple

import torchvision.transforms.v2 as T
from torch import Tensor
from torchvision.tv_tensors import BoundingBoxes, Image, Mask
from detectools.formats import Format, SegmentationFormat
from detectools.formats.detect_mask import DetectMask


class Augmentation:
    """Augmentation class allow augmentation of both images and targets as BaseFormat.

    Args:
            augmentations (``List[T.Transform]``, **optional**): List of torchvision v2 transforms. Defaults to [].
    
     Attributes
    ----------

    Attributes:
        transform (``T.Compose``): Composition of torchvision transforms.
    
    Methods
    ----------
    """
    def __init__(self, augmentations: List[T.Transform] = []):

        # Make the compose of all the augmentations
        self.transform = T.Compose(augmentations)

    def __call__(self, image: Tensor, target: Format) -> Tuple[Tensor, Format]:
        """Apply  transformations to image & target and return augmented pair.

        Args:
            image (``Tensor``): RGB Tensor image.
            target (``Format``): Target as BaseFormat.

        Returns:
            ``Tuple[Tensor, Format]``:
                - Augmented image.
                - Augmented target.
        """
        
        # send image & annotations to TVTensors
        image = Image(image)
        labels, boxes = target.get("labels", "boxes")
        boxes: BoundingBoxes = target.get("boxes")
        # wrap into list
        originals = [image, labels, boxes]
        if isinstance(target, SegmentationFormat):
            originals.append(Mask(target.get("masks")._mask))
        # apply augmentation
        transformed = self.transform(*originals)

        # create augmented_target
        augmented_target = target.clone()
        augmented_image, augmented_labels, augmented_boxes = transformed[:3]
        augmented_boxes: BoundingBoxes
        spatial_size = augmented_boxes.canvas_size
        # pass augmented values in augmented target 
        augmented_target.set("boxes", augmented_boxes)
        augmented_target.set("labels", augmented_labels)
        augmented_target.spatial_size = spatial_size
        augmented_target.spatial_size = augmented_boxes.canvas_size
        
        if isinstance(augmented_target, SegmentationFormat):
            augmented_masks = DetectMask(transformed[3])
            keep_index = augmented_masks.reindex()
            augmented_target = augmented_target[keep_index]
            augmented_target.set("masks", augmented_masks)

        return augmented_image, augmented_target
