from __future__ import annotations

from typing import Any, Dict, List, Tuple

from detectools import Task
from detectools.formats.base import BaseAnnotation, BaseFormat
from detectools.formats.detection_format import (DetectionAnnotation,
                                                 DetectionFormat)
from detectools.formats.segmentation_format import (SegmentationAnnotation,
                                                    SegmentationFormat)


class Format(BaseFormat):
    """Format class send either to ``DetectionFormat`` or ``SegmentationFormat`` depending on the Task mode.

    Returns:
        ``BaseFormat``:
            - BaseFormat instance.

    Methods
    -----------
    """

    def __new__(self, *args, **kwargs) -> BaseFormat:
        if Task.mode == "instance_segmentation":
            return SegmentationFormat(*args, **kwargs)
        else:
            return DetectionFormat(*args, **kwargs)

    def from_coco(
        coco_annotations: List[Dict[str, Any]], spatial_size: Tuple[int]
    ) -> BaseFormat:
        """Return one of the BaseFormats (DetectionFormat or SegmentationFormat depending on the Task mode) from an image COCO data dictionnary.

        Args:
            coco_annotations (``List[Dict[str, Any]]``): Coco data dictionnary.
            spatial_size (``Tuple[int]``): Size (H, W) of the corresponding image.

        Returns:
            ``BaseFormat``:
                - BaseFormat instance.
        """
        if Task.mode == "instance_segmentation":
            return SegmentationFormat.from_coco(coco_annotations, spatial_size)
        else:
            return DetectionFormat.from_coco(coco_annotations, spatial_size)

    def empty(spatial_size: Tuple[int]) -> BaseFormat:
        """Return an empty instance of BaseFormat (DetectionFormat or SegmentationFormat depending on the Task mode).

        Args:
            spatial_size (``Tuple[int]``): Size (H, W) of the corresponding image.

        Returns:
            ``BaseFormat``:
                - BaseFormat instance.
        """
        if Task.mode == "instance_segmentation":
            return SegmentationFormat.empty(spatial_size)
        else:
            return DetectionFormat.empty(spatial_size)


class Annotation(BaseAnnotation):
    """Return one of the ``BaseFormat`` (``DetectionAnnotation`` or ``SegmentationAnnotation`` depending on the Task mode).

    Returns:
        ``BaseAnnotation``:
            - BaseAnnotation instance.
    """

    def __new__(self, *args, **kwargs) -> BaseAnnotation:
        
        if Task.mode == "instance_segmentation":
            return SegmentationAnnotation(*args, **kwargs)
        else:
            return DetectionAnnotation(*args, **kwargs)


class BatchedFormats:
    """BatchedFormats wrap multiple Formats in a batch. BaseFormats should be passed in the same order than the images in images batch.

    Args:
        formats (``List[BaseFormat]``): List of BaseFormats to batchify.

    Attributes:
    -----------

    Attributes:
        formats (``Dict[str, BaseFormat]``): All BaseFormats contained in a dict with corresponding images index in keys.
        spatial_size (``Tuple[int,int]``)

    Methods:
    -----------
    """

    formats: Dict[str, BaseFormat]
    spatial_size: Tuple[int, int]

    def __init__(self, formats: List[BaseFormat]):

        n_formats = len(formats)
        # wrap formats in dict
        self.formats = dict(zip(range(n_formats), formats))
        self.set_spatial_size()

    def split(self) -> List[BaseFormat]:
        """Return list of BaseFormats following the order in formats attribute.

        Returns:
            ``List[BaseFormat]``:
                - List of BaseFormats.
        """
        return list(self.formats.values())

    def clone(self) -> BatchedFormats:
        """Clone a BatchedFormats instance.

        Returns:
            ``BatchedFormats``:
                - Cloned BatchedFormats instance.
        """
        clones = list(self.formats.values())
        clones = [c.clone() for c in clones]
        clone = BatchedFormats(clones)

        return clone

    def apply(self, method_name: str, *args, **kwargs):
        """
        Apply a function to all formats contained in formats attributes. **args** and **kwargs** are the parameters of the function to use.

        Args:
            method_name (``str``): BaseFormat method name.
        """
        for k, f in self.formats.items():
            # gather method object
            method = f.__getattribute__(method_name)
            # apply method to format
            output = method(*args, **kwargs)
            # if method output modified format, replace it
            if isinstance(output, BaseFormat):
                self.formats[k] = output

    def get_attributes(self, attribute: str, *args, **kwargs) -> List[Any]:
        """Return a list of Format attribute, one for each Format in BatchedFormats.

        Args:
            attribute (``str``): Attribute name.

        Returns:
            ``List[Any]``: List of attribute values for each Format.
        """
        outputs = []
        for f in self.formats.values():
            # gather method object
            attr = f.__getattribute__(attribute)
            outputs.append(attr)

        return outputs

    def set_spatial_size(self):
        """Check if all internal Formats have the same spatial_size & set this spatial_size as BatchedFormat spatial_size."""

        spatial_sizes = [f.spatial_size for f in self.formats.values()]
        batch_spatial_size = set(spatial_sizes)
        assert (
            len(batch_spatial_size) == 1
        ), f"All spatial_sizes should be equal to batchify multiple Formats, got {batch_spatial_size}"
        self.spatial_size = list(batch_spatial_size)[0]
