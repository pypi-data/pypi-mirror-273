from typing import List, Tuple

import cv2
import numpy as np
import torch
from torch import Tensor
from pycocotools import mask as mask_utils
from typing import Any, List, Literal

def cocopolygons2mask(polygons: List, size: Tuple[int]) -> Tensor:
    """Convert coco segmentation polygons to binary masks.

    Args:
        polygons (``List``): List of coco polygons.
        size (``Tuple[int]``): size of corresponding image (H, W).

    Returns:
        ``Tensor``:
            - Binary mask of shape (H, W).
    """
    finale_polygon = []
    mask = np.zeros(size, dtype=np.int32)
    # extract full polygon in list[subpolygons]
    for seg in polygons:
        finale_polygon.append(np.array(seg).astype("int64").reshape(int(len(seg) / 2), 2))
    # convert polygon to a final mask
    mask = cv2.fillPoly(mask, finale_polygon, 1)
    return torch.tensor(mask)

def cocoseg2masks(segmentation: Any, mask_size: Tuple[int]) -> Tensor:
    """From COCO segmentation return mask.

    Args:
        segmentation (``Any``): Segmentation in COCO json (polygons, compressed RLE or uncompressed RLE).
        mask_size (``Tuple[int]``): H, W shape of image.

    Returns:
        ``Tensor``:
            - Binary mask (H, W).
    """

    if isinstance(segmentation, list):
        mask = cocopolygons2mask(segmentation, mask_size)
    elif isinstance(segmentation, dict) and "counts" in segmentation.keys():
        if isinstance(segmentation["counts"], list):
            mask = uncompressed_rle_to_mask(segmentation)
        elif isinstance(segmentation["counts"], str):
            mask = mask_utils.decode()
    
    return mask

def uncompressed_rle_to_mask(uncompressed_rle: Any) -> Tensor:
    """From uncompressed RLE segmentation return mask.

    Args:
        uncompressed_rle (``Any``): Uncompressed RLE mask encoding.

    Returns:
        ``Tensor``:
            - Binary mask (H, W).
    """
    h, w = uncompressed_rle["size"][:2]
    compressed_rle = mask_utils.frPyObjects(uncompressed_rle, h,w)
    binary_mask = torch.tensor(mask_utils.decode(compressed_rle))
    return binary_mask


def mask2polygons(mask: Tensor) -> Tuple[List[List], float]:
    """convert one mask to polygon for coco export

    Args:
        mask (``Tensor``): Binary mask.

    Returns:
        ``Tuple[List[List], float]``:
            - List of polygons (one by continuous mask), area.
    """
    if mask.ndim == 0:
        segmentation = [[]]
        area = 0
        return segmentation, area
    
    if mask.ndim == 3:
        mask.squeeze()
    # detect contours
    mask = mask.cpu().numpy()
    contours, _ = cv2.findContours(
        mask.astype("uint8"),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # store polygons and compute area
    segmentation = [object.flatten().tolist() for object in contours]
    area = sum([cv2.contourArea(contour) for contour in contours])

    return segmentation, area
