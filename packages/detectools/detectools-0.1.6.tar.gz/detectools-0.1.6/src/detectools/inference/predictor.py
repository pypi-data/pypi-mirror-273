from math import ceil
from typing import Callable, List, Literal, Tuple, Union

import torch
from computervisiontools import load_image, save_image
from computervisiontools.preprocessing import build_preprocessing
from detectools.formats import BaseFormat
from detectools.inference.engine import patchification, unpatchification
from detectools.models import BaseModel
from detectools.visualisation import visualisation
from torch import Tensor
from torch.utils.data import DataLoader, TensorDataset


class InferenceImage:
    """Class to process patchification/unpatchification in inference pipeline. Pacthification is automatically done during construction.

    Args:
        image (``Tensor``): Image to predict on.
        patch_size (``_type_``, **optional**): Patch size to predict with model forward pass. Defaults to Tuple[int].
        overlap (``float``, **optional**): Proportion of overlap between patches. Defaults to 0.0.

    Attributes:
    -----------

    Attributes:
        patch_size (``Tuple[int, int]``): Size of patch to slice original image.
        size (``Tuple[int, int]``): Size of original image.
        overlap (``List[Tuple[int, int]]``): List of to left corner patches coordinates.
        padded_size (``Tuple[int, int]``): Size of padded image to patchify.

    Methods:
    -----------

    """

    patch_size: Tuple[int, int]
    size: Tuple[int, int]
    overlap: float
    patches: Tensor
    coordinates: List[Tuple[int, int]]
    padded_size: Tuple[int, int]

    def __init__(
        self,
        image: Tensor,
        patch_size=Tuple[int],
        overlap: float = 0.0,
    ):

        # store original image size
        self.size = image.shape[-2:]
        self.patch_size = patch_size
        self.overlap = overlap
        # process patchification and store patches coords and padded size
        self.patches, self.coordinates, self.padded_size = patchification(
            image, patch_size, overlap
        )

    def get_patches(self) -> TensorDataset:
        """Return patches as TensorDataset for batchification.

        Returns:
            ``TensorDataset``:
                -  Patches Dataset.
        """
        return TensorDataset(self.patches)

    def rebuild_prediction(self, predictions: List[BaseFormat]) -> BaseFormat:
        """Merge predictions at corresponding positions the retroieve original image size by cropping predictions.

        Args:
            predictions (``List[Format]``): Patches predictions.

        Returns:
            ``Format``:
                - Prediction rebuilt at original image size.
        """
        # merge patches predictions
        prediction = unpatchification(predictions, self.coordinates, self.padded_size)
        pad_h, pad_w = self.padded_size
        h, w = self.size
        # crop padded predictions to fit original size
        top, left, height, width = ceil((pad_h - h) / 2), ceil((pad_w - w) / 2), h, w
        prediction.crop(top, left, height, width)
        return prediction


class Predictor:
    """Predictor class wrap whole inference process to predict on images, including large images with patchification process.

    Args:
        model (``BaseModel``): Model from detectools.
        patch_size (``Tuple[int]``, **optional**): Size of patch to predict on, if None patch_size = image_size. Defaults to None.
        overlap (``float``, **optional**): Size of patches to patchify large image, if 0.0 no patchification done. Defaults to 0.0.
        nms_thr (``float``, **optional**): IoU threshold to consider 2 boxes as overlapping in NMS algorithm. Defaults to 0.45.
        confidence_thr (``float``, **optional**): Minimum confidence score to keep predicted objects. Defaults to 0.5.
        max_detection (``int``, **optional**): Maximum objects to keep in each prediction, the ones with higer scores are kept. Defaults to 300.
        batch_size (``int``, **optional**): Batch size for inference process, patches will be process in batch. Defaults to 16.
        preprocessing (``Callable``, **optional**): Preprocessing function to prepare image. Defaults to build_preprocessing().
        device (``Literal['cpu', 'cuda']``, **optional**): Device to use for prediction. Defaults to "cpu".

    Example: Predict on image.
    --------------------------

    .. highlight:: python
    .. code-block:: python

        >>> from detectools.predictor import Predictor
        >>> from detectools import write_json
        >>> import torch
        >>> model = torch.load("/path/to/model.pth")
        >>> predictor = Predictor(model=model)
        >>> predictions = predictor.predict("/path/to/rgb/image.png")
        >>> pred_coco_dict = predictions.coco()
        >>> write_json("/path/to/output.json", pred_coco_dict)

    Attributes:
    -----------

    Attributes:

        model (``BaseModel``): Model from detectools.
        patch_size (``Tuple[int]``): Size of patch to predict on, if None, patch_size == image_size. Defaults to None.
        overlap (``float``): Size of patches to patchify large image, if 0.0 no patchification done. Defaults to 0.0.
        nms_thr (``float``): IoU threshold to consider 2 boxes as overlapping in NMS algorithm. Defaults to 0.45.
        confidence_thr (``float``): Minimum confidence score to keep predicted objects. Defaults to 0.5.
        max_detection (``int``): Maximum objects to keep in each prediction, the ones with higer scores are kept. Defaults to 300.
        batch_size (``int``,): Batch size for inference process, patches will be process in batch. Defaults to 16.
        preprocessing (``Callable``): Preprocessing function to prepare image. Defaults to build_preprocessing().
        device (``Literal['cpu', 'cuda']``): Device to use for prediction. Defaults to "cpu".

    Methods:
    --------
    """

    model: BaseModel
    patch_size: Tuple[int]
    overlap: float
    nms_thr: float
    confidence_thr: float
    max_detection: int
    batch_size: int
    preprocessing: Callable
    device: Literal["cpu", "cuda"]

    def __init__(
        self,
        model: BaseModel,
        patch_size: Tuple[int] = None,
        overlap: float = 0.0,
        nms_thr: float = 0.45,
        confidence_thr: float = 0.5,
        max_detection: int = 300,
        batch_size: int = 16,
        preprocessing: Callable = build_preprocessing(),
        device: Literal["cpu", "cuda"] = "cpu",
    ):

        self.model = model.eval()
        self.model.to_device(device)
        self.model.confidence_thr = confidence_thr
        self.model.nms_threshold = nms_thr
        self.model.max_detection = max_detection
        self.overlap = overlap
        self.nms_thr = nms_thr
        self.confidence_thr = confidence_thr
        self.batch_size = batch_size
        self.preprocessing = preprocessing
        self.device = device
        self.patch_size = patch_size

    def forward_pass(self, batch_patchs: Tensor) -> List[BaseFormat]:
        """Get predictions for patches.

        Args:
            batch_patchs (``Tensor``): Batch of image patches.

        Returns:
            ``List[BaseFormat]``:
                - Patches predictions.
        """
        with torch.no_grad():
            predictions = self.model.get_predictions(batch_patchs)
            # split in N predictions for N == batch size (avoid forgetting empty predictions)
            return predictions.split()

    def predict(
        self, image: Union[Tensor, str], visualisation_path: str = ""
    ) -> BaseFormat:
        """Predict on image.

        Args:
            image (``Union[Tensor, str]``): Image to predict. If is a path, load image and predict on it.
            visualisation_path (``str``, **optional**): Path to save prediction visualisation. Defaults to "" (no visualisation).. Defaults to "".

        Returns:
            ``BaseFormat``:
                - Prediction.
        """
        # if image is a file load image as Tensor
        if isinstance(image, str):
            image = load_image(image)
        # send to device
        image = image.to(self.device)
        # apply preprocessing
        image_prepared: Tensor = self.preprocessing(image)
        # create inference image with patchification
        patch_size = self.patch_size if self.patch_size else image_prepared.shape[-2:]
        inference_image = InferenceImage(image_prepared, patch_size, self.overlap)
        # predict on patches
        patches = DataLoader(inference_image.get_patches(), batch_size=self.batch_size)
        batch_predictions = [self.forward_pass(batch[0]) for batch in patches]
        patches_prediction = [p for b in batch_predictions for p in b]
        # merge patches predictions
        image_prediction = inference_image.rebuild_prediction(patches_prediction)
        # re run nms for != patches objects overlapping
        if image_prediction.size > 0:
            image_prediction = image_prediction.nms(self.nms_thr)
        # do visualisation & save it
        if visualisation_path:
            visu = visualisation(image, image_prediction)
            save_image(visu, visualisation_path)

        return image_prediction
