# -*- coding: utf-8 -*-

"""Torch prebuild functions to train, evaluate and use models in production."""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Literal, Union

__version__ = "0.1.6" # change detectools version here

IMAGE_FOLDER = "images"
ANNOTATION_FILE = "coco_annotations.json"

COLORS = [
    (0, 102, 204),
    (51, 255, 51),
    (255, 0, 0),
    (51, 51, 255),
    (255, 51, 255),
    (255, 255, 0),
    (86, 255, 255),
    (100, 200, 100),
    (250, 50, 125),
    (125, 250, 0),
    (125, 50, 250),
    (125, 125, 125),
    (20, 20, 200),
]  # set of colors for visualisation (max 13 classes for now)


class Task:
    """Task define the mode of the library to use. If 'detection' masks will not be take, if 'instance segmentation' masks will be handle.

    Attributes
    ----------

    Attributes:
        mode: Literal['detection', 'instance segmentation]
    
    Methods
    ----------
    """
    mode = "detection"

    def set_mode(cls, mode: Literal["detection", "instance_segmentation"]):
        """Set Task mode.

        Args:
            mode (``Literal['detection', 'instance_segmentation']``): Mode to use.
        """
        cls.mode = mode


def set_lib_mode(mode: Literal["detection", "instance_segmentation"]):
    """Set global mode for library.

    Args:
        mode (``Literal['detection', 'instance_segmentation']``): Mode for library.
    """
    Task.set_mode(Task, mode)
