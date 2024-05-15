from __future__ import annotations

from detectools.formats.base import BaseAnnotation, BaseFormat
from detectools.formats.detection_format import DetectionAnnotation, DetectionFormat
from detectools.formats.interfaces import Annotation, BatchedFormats, Format
from detectools.formats.segmentation_format import (
    SegmentationAnnotation,
    SegmentationFormat,
)
from detectools.formats.detect_mask import DetectMask

__all__ = (
    "BaseAnnotation",
    "BaseFormat",
    "DetectionAnnotation",
    "DetectionFormat",
    "SegmentationAnnotation",
    "SegmentationFormat",
    "Format",
    "Annotation",
    "BatchedFormats",
    "DetectMask"
)  # allow simpler import
